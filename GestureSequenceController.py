import cStringIO
import Log

class GestureSequenceController:
    def __init__ (self, config_json, call_upon_activation = None):
        bindings = config_json['bindings']
        sequences = [(tuple(GestureSequenceController.__parse_gesture_string(gesture_string) for gesture_string in binding['sequence']), binding['action']) for binding in bindings]

        self.__sequences = sequences
        self.__call_upon_activation = call_upon_activation
        self.reset_active_sequences()
    
    def process_gesture (self, gesture_string):
        Log.record('process_gesture("{0}")\n'.format(gesture_string))
        Log.indent()
        
        winning_sequence = None
        sequences_to_eliminate = set()

        handedness,gesture_name = GestureSequenceController.__parse_gesture_string(gesture_string)
        Log.record('handedness = {0}, gesture_name = {1}\n'.format(handedness, gesture_name))

        Log.record('active sequences before processing:\n')
        Log.indent()
        Log.record(self.__active_sequences_as_string())
        Log.unindent()

        Log.record('running through active sequences\n')
        Log.indent()
        for sequence,current_index in self.__active_sequences.iteritems():
            sequence_item = sequence[0][current_index]
            satisfies_handedness_requirement = sequence_item[0] == None or (sequence_item[0] != None and sequence_item[0] == handedness)
            satisfies_gesture_name_match_requirement = sequence_item[1] == gesture_name
            if satisfies_handedness_requirement and satisfies_gesture_name_match_requirement:
                self.__active_sequences[sequence] += 1
                current_index = self.__active_sequences[sequence]
                if current_index == len(sequence[0]):
                    Log.record('sequence {0} recognized -- key combo: "{1}"'.format(sequence[0], sequence[1]))
                    if winning_sequence == None:
                        Log.record(' ... setting as winning sequence\n')
                        winning_sequence = sequence
                    else:
                        Log.record('\n')
            else:
                sequences_to_eliminate.add(sequence)
        for sequence in sequences_to_eliminate:
            del self.__active_sequences[sequence]
        Log.unindent()
        
        Log.record('active sequences after processing:\n')
        Log.indent()
        Log.record(self.__active_sequences_as_string())
        Log.unindent()

        if winning_sequence != None:
            if len(self.__active_sequences) > 1:
                Log.record('WARNING: Conflicting sequences:\n')
                Log.indent()
                for sequence in self.__active_sequences:
                    Log.record('{0}'.format(sequence))
                Log.unindent()
                Log.record('Using first-declared sequence {0}\n'.format(winning_sequence))
            if self.__call_upon_activation != None:
                self.__call_upon_activation(winning_sequence[1])
            self.reset_active_sequences()
        elif len(self.__active_sequences) == 0:
            self.reset_active_sequences()
        
        Log.unindent()
    
    def reset_active_sequences (self):
        self.__active_sequences = {sequence:0 for sequence in self.__sequences}
        self.__active_sequences_as_string()
    
    def __active_sequences_as_string (self):
        output_stream = cStringIO.StringIO()
        for sequence,current_index in self.__active_sequences.iteritems():
            output_stream.write('{0}:{1}\n'.format(sequence, current_index))
        return output_stream.getvalue()

    @staticmethod
    def __parse_gesture_string (gesture_string):
        """
        A gesture string has the form "lefthand:gesturename" or "righthand:gesturename" or "gesturename".
        """
        g = gesture_string.split(":", 1) # Split at most once.
        if len(g) == 1:
            handedness = None
            gesture_name = g[0]
        elif len(g) == 2:
            handedness = g[0]
            gesture_name = g[1]
        else:
            raise Exception('Invalid gesture string.  Must have the form "lefthand:gesturename" or "righthand:gesturename" or "gesturename".')
        return handedness,gesture_name
