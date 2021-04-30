from __future__ import absolute_import

"""
Note that 'unicode_literals' is NOT used in by this module.  This is on
purpose.  Using the Python 2/3 default for 'str' works perfectly here.  This
limitation is due to same bad behavior in the Splunk SDK, IMHO.
"""

from logging import getLogger

# Apply fixes to splunk-sdk; this MUST occur before loading splunklib
import cypresspoint.monkeypatch  # noqa

from splunklib.modularinput import Script  # noqa

HIDDEN_PASSWORD = "*" * 8


class ScriptWithSimpleSecret(Script):
    """ Class that extends Splunk's default 'Script' that allows for very basic
    storage of a secret value.  Note that this techincally results in a
    race-condition where the unencrypted secret is exposed for some short period
    of time.  Therefore this shouldn't be used in high security scenarios or on
    servers with many snooping users, but for private use apps on a dedicated
    data onboarding forwarder, this approach is often "good enough".
    """
    secret_field = "secret"

    def __init__(self, *args, **kwargs):
        super(ScriptWithSimpleSecret, self).__init__(*args, **kwargs)
        self.logger = getLogger(self.__class__.__name__)

    def handle_secret(self, input_name, password, app=None):
        """
        Get, Set, or Update secret field as needed.

        This command will encrypt any clear-text password and mask it's value in
        ``inputs.conf``.  If a clear-text password is not given, then it's assumed
        to have been previously saved and will be loaded from ``passwords.conf``

        :param str input_name: Stanza in ``inputs.conf`` of the modular input
        :param str password: The recipient of the message
        :param app: The splunk app namesspace to use for REST interactions
                    against inputs and password endpoints
        :type app: str or None
        :return: the clear-text password
        :rtype: str
        """
        # type: (str, str, str) -> str
        if app:
            self.service.namespace.app["app"] = app
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
            stanza.update(api_key=HIDDEN_PASSWORD)
            logger.info("Updated inputs.conf [%s] %s=%s", input_name, field, HIDDEN_PASSWORD)
            return password
