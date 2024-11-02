from dataclasses import dataclass
from xml.etree import ElementTree as ET

from bytecode.score.utils import Duration


@dataclass
class Note:
    pitch: int
    duration: int


class Voice:

    def __str__(self):
        out = f"Voice(Notes: "
        for note in self.notes:
            out += str(note) + ", "
        return out[:-2] + ")"

    @property
    def time_sig(self):
        return int(16 * self.time_sig_n / self.time_sig_d)

    def __init__(self, voice_elm: ET.Element, time_sig: int|None = None):
        if time_sig is not None:
            self.time_sig = time_sig
        self.notes: list[Note] = []
        for child in voice_elm:
            if child.tag == "TimeSig":
                print("TimeSig")
                for grand_child in child:
                    if grand_child.tag == "sigN":
                        self.time_sig_n = int(grand_child.text)
                    if grand_child.tag == "sigD":
                        self.time_sig_d = int(grand_child.text)
            elif child.tag == "Chord":
                ticks = 0
                for grand_child in child:
                    if grand_child.tag == "durationType":
                        ticks = Duration.parse_duration(grand_child.text)
                    if grand_child.tag == "Note":
                        for great_grand_child in grand_child:
                            if great_grand_child.tag == "pitch":
                                self.notes.append(
                                    Note(int(great_grand_child.text), ticks))
            elif child.tag == "Rest":
                self.notes.append(Note(-1, self.time_sig))
        return self.time_sig


class Measure:

    def __str__(self):
        out = f"Measure(Voices: "
        for voice in self.voices:
            out += str(voice) + ", "
        return out[:-2] + ")"

    def __init__(self, measure_elm: ET.Element):
        self.voices: list[Voice] = []
        for child in measure_elm:
            if child.tag == "voice":
                self.voices.append(Voice(child))


class Staff:

    def __str__(self):
        out = f"Staff(Measures: "
        for measure in self.measures:
            out += str(measure) + ", "
        return out[:-2] + ")"

    def __init__(self, staff_elm: ET.Element):
        self.measures: list[Measure] = []
        for child in staff_elm:
            if child.tag == "Measure":
                self.measures.append(Measure(child))


class Score:

    def __str__(self):
        out = "Score("
        for staff in self.staffs:
            out += str(staff) + ", "
        return out[:-2] + ")"

    def __init__(self, score_elm: ET.Element):
        self.staffs: list[Staff] = []
        for child in score_elm:
            if child.tag == "Staff":
                self.staffs.append(Staff(child))
