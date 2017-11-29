#! -*- coding:utf-8 -*-
import salt.config
import salt.key

class saltMinionAuth:
    def __init__(self):
        self.opts = salt.config.master_config('/etc/salt/master')

    def authPassMinion(self):
        # return auth pass minion
        try:
            return salt.key.Key(opts=self.opts).list_keys()['minions']
        except Exception:
            pass

    def authWaitMinion(self):
        # return auth wait minion
        try:
            return salt.key.Key(opts=self.opts).list_keys()['minions_pre']
        except Exception:
            pass

    def authMinion(self, mon):
        try:
            if mon in self.authWaitMinion():
                salt.key.Key(opts=self.opts).accept(match=mon)
        except Exception:
            pass
