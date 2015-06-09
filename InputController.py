import Log
import pykeyboard
import time

class InputController:
    """
    This class provides facilities for generating keyboard and mouse events.
    It is a light abstraction of PyKeyboard and PyMouse.
    """
    def __init__ (self):
        self.__init_keyboard()
    
    def activate_key_combo (self, combo_string):
        Log.record('activate_key_combo("{0}")\n'.format(combo_string))
        Log.indent()
        # Parse the string which is delimited by + characters.
        key_actions = combo_string.split('+')
        # First pass of key processing -- press and release keys in order.
        # Note regarding the calls to time.sleep -- there was a use case where an 'alt+tab'
        # key combo would be effectively just 'tab' unless these calls were made to space
        # the key events out in time.
        for key_action in key_actions:
            s = key_action.split(':', 1) # Split at most once.
            key_name = s[0]
            key = self.key_map[key_name]
            release = len(s) == 2 and s[1] == "release"
            if release:
                self.release_key_if_held(key)
                time.sleep(0.01) # See note above
            press = len(s) == 1 or (len(s) == 2 and s[1] == "hold")
            if press:
                self.press_key_if_not_already_held(key)
                time.sleep(0.01) # See note above
        # Second pass -- release the keys that don't have a :hold or :release qualifier.
        for key_action in reversed(key_actions):
            s = key_action.split(':', 1) # Split at most once.
            key_name = s[0]
            key = self.key_map[key_name]
            release = len(s) == 1
            if release:
                self.release_key_if_held(key)
                time.sleep(0.01) # See note above
        Log.unindent()

    def press_key_if_not_already_held (self, key):
        if key not in self.held_keys:
            Log.record('pressing key {0}\n'.format(self.key_map_inverse[key]))
            self.keyboard.press_key(key)
            self.held_keys.add(key)

    def release_key_if_held (self, key):
        if key in self.held_keys:
            Log.record('releasing key {0}\n'.format(self.key_map_inverse[key]))
            self.keyboard.release_key(key)
            self.held_keys.remove(key)

    def release_all_held_keys (self):
        Log.record('release_all_held_keys()\n')
        Log.indent()
        for key in self.held_keys:
            Log.record('releasing key {0}'.format(self.key_map_inverse[key]))
            self.keyboard.release_key(key)
        self.held_keys.clear()
        Log.unindent()

    def set_mouse_position (self, normalized_position):
        """normalized_position must be a 2-tuple whose elements are in the range [0.0, 1.0]."""
        assert len(normalized_position) == 2
        assert 0.0 <= normalized_position[0] <= 1.0
        assert 0.0 <= normalized_position[1] <= 1.0
        screen_size = self.mouse.screen_size()
        x = int(round(normalized_position[0]*screen_size[0]))
        y = int(round(normalized_position[1]*screen_size[1]))
        self.mouse.move(x,y)

    def __init_keyboard (self):
        self.keyboard = pykeyboard.PyKeyboard()
        k = self.keyboard
        self.key_map = { \
            'accept'        :k.accept_key, \
            'alt'           :k.alt_key, \
            'left-alt'      :k.alt_l_key, \
            'right-alt'     :k.alt_r_key, \
            'apps'          :k.apps_key, \
            'backspace'     :k.backspace_key, \
            'begin'         :k.begin_key, \
            'break'         :k.break_key, \
            'cancel'        :k.cancel_key, \
            'capital'       :k.capital_key, \
            'caps-lock'     :k.caps_lock_key, \
            'clear'         :k.clear_key, \
            'control'       :k.control_key, \
            'left-control'  :k.control_l_key, \
            'right-control' :k.control_r_key, \
            'convert'       :k.convert_key, \
            'delete'        :k.delete_key, \
            'down'          :k.down_key, \
            'end'           :k.end_key, \
            'enter'         :k.enter_key, \
            'escape'        :k.escape_key, \
            'execute'       :k.execute_key, \
            'final'         :k.final_key, \
            'find'          :k.find_key, \
            'hangeul'       :k.hangeul_key, \
            'hangul'        :k.hangul_key, \
            'hanja'         :k.hanja_key, \
            'help'          :k.help_key, \
            'home'          :k.home_key, \
            'left-hyper'    :k.hyper_l_key, \
            'right-hyper'   :k.hyper_r_key, \
            'insert'        :k.insert_key, \
            'junjua'        :k.junjua_key, \
            'kana'          :k.kana_key, \
            'kanji'         :k.kanji_key, \
            'left'          :k.left_key, \
            'linefeed'      :k.linefeed_key, \
            'menu'          :k.menu_key, \
            'left-meta'     :k.meta_l_key, \
            'right-meta'    :k.meta_r_key, \
            'mode-switch'   :k.mode_switch_key, \
            'mode-change'   :k.modechange_key, \
            'next'          :k.next_key, \
            'nonconvert'    :k.nonconvert_key, \
            'num-lock'      :k.num_lock_key, \
            'page-down'     :k.page_down_key, \
            'page-up'       :k.page_up_key, \
            'pause'         :k.pause_key, \
            'print'         :k.print_key, \
            'print-screen'  :k.print_screen_key, \
            'prior'         :k.prior_key, \
            'redo'          :k.redo_key, \
            'return'        :k.return_key, \
            'right'         :k.right_key, \
            'script-switch' :k.script_switch_key, \
            'scroll-lock'   :k.scroll_lock_key, \
            'select'        :k.select_key, \
            'shift'         :k.shift_key, \
            'left-shift'    :k.shift_l_key, \
            'shift-lock'    :k.shift_lock_key, \
            'right-shift'   :k.shift_r_key, \
            'sleep'         :k.sleep_key, \
            'snapshot'      :k.snapshot_key, \
            'left-super'    :k.super_l_key, \
            'right-super'   :k.super_r_key, \
            'sys-req'       :k.sys_req_key, \
            'tab'           :k.tab_key, \
            'undo'          :k.undo_key, \
            'up'            :k.up_key, \
            'left-windows'  :k.windows_l_key, \
            'right-windows' :k.windows_r_key
        }
        # Add the standard typeable keys.
        self.key_map['space'] = ' '
        for c in "`1234567890[]',.pyfgcrl/=\\aoeuidhtns-;qjkxbmwvz":
            self.key_map[c] = c
        # Add the function keys.
        for i,key in enumerate(k.function_keys):
            if key != None and key != 0:
                self.key_map['f{0}'.format(i)] = key
        # Add the numpad keys.
        for name,key in k.numpad_keys.iteritems():
            if isinstance(name,str):
                name = name.replace('_','-').lower()
            self.key_map['numpad-{0}'.format(name)] = key

        # Delete unsupported keys.
        Log.record('Identifying unsupported keys.\n')
        Log.indent()
        keys_to_delete = []
        for name,key in self.key_map.iteritems():
            if key == 0 or key == None:
                Log.record("key '{0}' is not available on this machine.\n".format(name))
                keys_to_delete.append(name)
        Log.unindent()
        for name in keys_to_delete:
            del self.key_map[name]
            
        #Log.record('key_map = {\n')
        #Log.indent()
        #for name,key in self.key_map.iteritems():
            #Log.record('{0}:{1},'.format(name,key))
        #Log.unindent()
        #Log.record('}')
        
        Log.record('Available key names: [\n')
        Log.indent()
        available_key_names = sorted(self.key_map.keys())
        for available_key_name in available_key_names:
            Log.record("'{0}',\n".format(available_key_name))
        Log.unindent()
        Log.record(']\n')

        # This is really just for printing the key names based on key codes.
        self.key_map_inverse = {key:name for name,key in self.key_map.iteritems()}
        #Log.record('{0}'.format(self.key_map_inverse))
        self.held_keys = set([])
