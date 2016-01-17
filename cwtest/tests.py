from unittest import TestCase
from cwtest.types import RoversHandler


class RoverTestCase(TestCase):
    def test_rovers_handling(self):
        rovers_handler = RoversHandler()
        lines = """
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
        """
        lines = filter(None, [line.strip() for line in lines.split('\n')])
        for line in lines:
            rovers_handler.process_line(line)

        output_lines = rovers_handler.get_output_lines()
        self.assertEquals(output_lines, ['1 3 N', '5 1 E'])
