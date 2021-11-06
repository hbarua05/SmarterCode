import manim as M
import subprocess
from scenes import SceneOne, SceneTwo, SceneThree, SceneFour, SceneFive


class Main(
        SceneOne,
        SceneTwo,
        SceneThree,
        SceneFour,
        SceneFive
):
    def construct(self):
        SceneOne.construct(self)
        self.play(M.FadeOut(*self.mobjects))
        SceneTwo.construct(self)
        self.play(M.FadeOut(*self.mobjects))
        SceneThree.construct(self)
        self.play(M.FadeOut(*self.mobjects))
        SceneFour.construct(self)
        self.play(M.FadeOut(*self.mobjects))
        SceneFive.construct(self)


if __name__ == "__main__":
    command = ["manim", __file__, "Main", "-pql"]
    print(" ".join(command))
    subprocess.run(command)
