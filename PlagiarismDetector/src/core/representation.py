from music21 import converter, note, chord

class MusicRepresentation:
    """Gestisce le 5 rappresentazioni delle melodie"""

    def __init__(self, midi_path):
        try:
            self.score = converter.parse(midi_path)
            self.notes_list = self._extract_notes()
        except Exception as e:
            raise ValueError(f"Errore nel caricamento del file: {e}")

    def _extract_notes(self):
        notes = []
        for element in self.score.flatten().notesAndRests:
            if isinstance(element, (note.Note, chord.Chord)):
                if isinstance(element, note.Note):
                    pitch = element.pitch.midi
                    name = element.pitch.nameWithOctave
                else:
                    pitch = element.pitches[0].midi
                    name = element.pitches[0].nameWithOctave

                notes.append({
                    'pitch': pitch,
                    'duration': element.quarterLength,
                    'note_name': name
                })
        return notes

    def transpose(self, semitones):
        return [
            {
                'pitch': n['pitch'] + semitones,
                'duration': n['duration'],
                'note_name': self._midi_to_note(n['pitch'] + semitones)
            }
            for n in self.notes_list
        ]

    @staticmethod
    def _midi_to_note(midi_num):
        notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        octave = (midi_num // 12) - 1
        return f"{notes[midi_num % 12]}{octave}"

    # =====================================================
    # 🚀 METODO VELOCE USATO DALLA GUI (QUESTO MANCAVA)
    # =====================================================
    def get_all_representations(self, notes_list=None):
        if notes_list is None:
            notes_list = self.notes_list

        return {
            'note': [n['note_name'] for n in notes_list],

            'interval': [
                notes_list[i]['pitch'] - notes_list[i - 1]['pitch']
                for i in range(1, len(notes_list))
            ],

            'duration': [n['duration'] for n in notes_list],

            'pitch_da': [
                (
                    notes_list[i]['pitch'] - notes_list[i - 1]['pitch'],
                    notes_list[i]['duration']
                )
                for i in range(1, len(notes_list))
            ],

            'pitch_nd': [
                (
                    1 if notes_list[i]['pitch'] - notes_list[i - 1]['pitch'] > 0
                    else -1 if notes_list[i]['pitch'] - notes_list[i - 1]['pitch'] < 0
                    else 0,
                    notes_list[i]['duration']
                )
                for i in range(1, len(notes_list))
            ]
        }
