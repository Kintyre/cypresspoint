from __future__ import absolute_import
# Note that 'unicode_literals' is NOT used in by this module.  This is on
# purpose.  Using the Python 2/3 default for 'str' works perfectly here.  This
# limitation is due to same bad behavior in the Splunk SDK, IMHO.

from logging import getLogger

# Apply fixes to splunk-sdk
import cypresspoint.monkeypatch  # nopep8

from splunklib.modularinput import Script


HIDDEN_PASSWORD = "*" * 8


class ScriptWithSimpleSecret(Script):
    """ Class that extends Splunk's default 'Script' that allows for very basic
    storage of a secrte value.  Note that this techincally results in a
    race-condition where the unencrypted secret is exposed for some short period
    oftime.  Therefore this shouldn't be used in high security scenarios or on
    highly active servers, but for private use apps, this is often "good enough".
    """
    secret_field = "secret"

    def __init__(self, *args, **kwargs):
        super(ScriptWithSimpleSecret, self).__init__(*args, **kwargs)
        self.logger = getLogger(self.__class__.__name__)

    def handle_secret(self, input_name, password):
        field = self.secret_field
        logger = self.logger
        scheme, name = input_name.split("://", 1)
        pw_name = "{}:{}".format(scheme, name)
        pw = self.service.storage_passwords
        if password == HIDDEN_PASSWORD:
            logger.debug("Grabbing %s from password store!", field)
            return pw[pw_name].clear_password
        else:
            try:
                p = pw[pw_name]
                if p.clear_password != password:
                    self.logger.info("Updated encrypted %s for input %s", field, input_name)
                    p.update(password=password)
                else:
                    # If this happens frequently without a password change this indicates a problem.
                    self.logger.info("Password update encountered;  No change made.")
            except KeyError:
                logger.info("Converting clear-text %s in inputs.conf to encrypted %s "
                            "store for input %s", field, field, input_name)
                pw.create(password, name, scheme)
            # Clear existing password in the input
            inputs = self.service.confs["inputs"]
            stanza = inputs[input_name]
            ##logger.debug("PW LEAK!!!! %r", stanza.content)
            stanza.update(api_key=HIDDEN_PASSWORD)
            logger.info("Updated inputs.conf [%s] %s=%s", input_name, field, HIDDEN_PASSWORD)
            return password
