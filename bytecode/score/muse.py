from xml.etree import ElementTree as ET

from bytecode.score.utils import Duration


class Voice:

    def __str__(self):
        out = f"Voice(Ticks: {self.ticks}, Pitches: "
        for pitch in self.pitches:
            out += f"{pitch}, "
        return out[:-2] + ") "

    def __init__(self, voice_elm: ET.Element):
        self.ticks: Duration = Duration.sixteenth
        self.pitches: list[int] = []
        for child in voice_elm:
            if child.tag == "Chord":
                for child in child:
                    if child.tag == "durationType":
                        self.ticks = Duration.parse_duration(child.text)
                    if child.tag == "Note":
                        for child in child:
                            if child.tag == "pitch":
                                self.pitches.append(int(child.text))


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
        out= f"Staff(Measures: "
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
