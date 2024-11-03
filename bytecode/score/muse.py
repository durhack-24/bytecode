from dataclasses import dataclass
from enum import EnumType
from xml.etree import ElementTree as ET

from bytecode.score.utils import Duration


class SlurState(EnumType):
    NO_SLUR = 0
    SLUR_START = 1
    SLUR_END = 2


@dataclass
class Note:
    pitch: int
    duration: int
    slur_state: int = SlurState.NO_SLUR


@dataclass
class RehearsalMark:
    text: str
    ticks: int


class Voice:

    def __str__(self):
        out = f"Voice(Notes: "
        for note in self.notes:
            out += str(note) + ", "
        return out[:-2] + " Rehearsal Mark: " + str(self.rehearsal_mark) + ")"

    @property
    def time_sig(self):
        try:
            return int(16 * self.time_sig_n / self.time_sig_d)
        except AttributeError as e:
            return self.previous_time_sig

    def __init__(self, voice_elm: ET.Element, time_sig: int = 16):
        self.previous_time_sig = time_sig
        self.notes: list[Note] = []
        self.rehearsal_mark = None
        for child in voice_elm:
            if child.tag == "TimeSig":
                for grand_child in child:
                    if grand_child.tag == "sigN":
                        self.time_sig_n = int(grand_child.text)
                    if grand_child.tag == "sigD":
                        self.time_sig_d = int(grand_child.text)
            elif child.tag == "RehearsalMark":
                for grand_child in child:
                    if grand_child.tag == "text":
                        self.rehearsal_mark = grand_child.text
            elif child.tag == "Chord":
                ticks = 0
                slur_state = SlurState.NO_SLUR
                for grand_child in child:
                    if grand_child.tag == "durationType":
                        ticks = Duration.parse_duration(grand_child.text)
                    if grand_child.tag == "Spanner":
                        if grand_child.attrib.get("type", "") == "Slur":
                            for great_grand_child in grand_child:
                                if great_grand_child.tag == "next":
                                    slur_state = SlurState.SLUR_START
                                if great_grand_child.tag == "prev":
                                    slur_state = SlurState.SLUR_END
                    if grand_child.tag == "Note":
                        for great_grand_child in grand_child:
                            if great_grand_child.tag == "pitch":
                                self.notes.append(
                                    Note(int(great_grand_child.text), ticks,
                                         slur_state=slur_state))

            elif child.tag == "Rest":
                ticks = self.time_sig
                for grand_child in child:
                    if grand_child.tag == "durationType":
                        if grand_child.text != "measure":
                            ticks = Duration.parse_duration(grand_child.text)
                        break
                self.notes.append(Note(-1, ticks))


class Measure:

    def __str__(self):
        out = f"Measure(Voices: "
        for voice in self.voices:
            out += str(voice) + ", "
        return out[:-2] + ")"

    def __init__(self, measure_elm: ET.Element):
        self.voices: list[Voice] = []
        previous_signature = 16
        for child in measure_elm:
            if child.tag == "voice":
                voice = Voice(child, previous_signature)
                previous_signature = voice.time_sig
                self.voices.append(voice)


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

    def get_notes(self):
        notes = []
        for measure in self.measures:
            for voice in measure.voices:
                for note in voice.notes:
                    notes.append(note)
        return notes

    def get_rehearsal_marks(self) -> list[RehearsalMark]:
        rehearsal_marks = []
        ticks = 0
        for measure in self.measures:
            for voice in measure.voices:
                ticks += voice.time_sig
                if voice.rehearsal_mark:
                    rehearsal_marks.append(
                        RehearsalMark(voice.rehearsal_mark, ticks))
        return rehearsal_marks


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
