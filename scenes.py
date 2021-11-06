import manim as M
from random import randint, shuffle


BITCOIN_YELLOW = "#f2a900"


def my_shuffle(array):
    shuffle(array)
    return array


class SceneOne(M.Scene):
    def construct(self):
        publication = M.ImageMobject("./assets/publication.png").scale(2)
        bitcoin_logo = M.SVGMobject("./assets/bitcoin.svg")\
            .scale(0.8).to_corner(M.UL)
        block_chain = BlockChain()
        self.play(
            M.FadeIn(publication, shift=M.UP),
            M.Create(bitcoin_logo),
            run_time=2,
        )
        self.wait()
        self.play(
            M.FadeOut(publication),
            bitcoin_logo.animate.move_to(M.ORIGIN),
            run_time=3
        )
        self.play(
            M.ReplacementTransform(bitcoin_logo, block_chain),
            run_time=2
        )
        self.wait()


class SceneTwo(M.Scene):
    def init_bitcoin_paths(self):
        node_positions = [
            2 * M.LEFT + 3 * M.UP,
            2 * M.RIGHT + 3 * M.UP,
            3 * M.LEFT,
            3 * M.RIGHT,
            2 * M.LEFT + 3 * M.DOWN,
            2 * M.RIGHT + 3 * M.DOWN,
        ]
        self.bitcoin_paths = []
        self.bitcoin_system = []

        for i in range(len(node_positions)):
            for k in range(i+1, len(node_positions)):
                path = M.Line(start=node_positions[i], end=node_positions[k])
                path.set_opacity(0.2)
                self.bitcoin_paths.append(path)

        for i in range(len(node_positions)):
            character = M.SVGMobject("./assets/person.svg").set_color(M.WHITE)
            character.scale(0.3)
            character.move_to(node_positions[i])
            self.bitcoin_system.append(character)

    def init_bank_paths(self):
        node_positions = {
            "bank": M.ORIGIN,
            "recipients":  [
                2 * M.LEFT + 3 * M.UP,
                2 * M.RIGHT + 3 * M.UP,
                3 * M.LEFT,
                3 * M.RIGHT,
                2 * M.LEFT + 3 * M.DOWN,
                2 * M.RIGHT + 3 * M.DOWN,
            ]

        }

        self.bank_paths = []
        self.bank_system = []

        for i in range(len(node_positions["recipients"])):
            path = M.Line(
                start=node_positions["bank"],
                end=node_positions["recipients"][i]
            )
            path.set_opacity(0.2)
            self.bank_paths.append(path)

        for i in range(len(node_positions["recipients"])):
            character = M.SVGMobject("./assets/person.svg").set_color(M.WHITE)
            character.scale(0.3)
            character.move_to(node_positions["recipients"][i])
            self.bank_system.append(character)

        bank = M.SVGMobject("./assets/bank.svg").set_color(M.LIGHTER_GRAY)
        bank.scale(0.5)
        self.bank_system.append(bank)

    def init_transfer_animations(self):
        self.bitcoin_transfer_animations = M.AnimationGroup(
            *[
                M.ShowPassingFlash(
                    self.bitcoin_paths[randint(0, len(self.bitcoin_paths)-1)]
                    .copy() .set_opacity(1).set_color(BITCOIN_YELLOW),
                    run_time=0.3
                )
                for _ in range(500)
            ],
            lag_ratio=0.1
        )

        self.bank_transfer_animations = M.AnimationGroup(
            *[
                M.ShowPassingFlash(
                    self.bank_paths[randint(0, len(self.bank_paths)-1)]
                    .copy().set_opacity(1).set_color(BITCOIN_YELLOW),
                    run_time=0.8
                )
                for _ in range(200)
            ],
            lag_ratio=0.1
        )

    def construct(self):
        self.init_bitcoin_paths()
        self.init_bank_paths()

        M.VGroup(
            M.VGroup(*self.bitcoin_paths, *self.bitcoin_system).scale(0.7),
            M.VGroup(*self.bank_paths, *self.bank_system).scale(0.7)
        ).arrange(buff=M.LARGE_BUFF * 3)

        self.init_transfer_animations()

        separator_line = M.Line(5 * M.UP, 5 * M.DOWN)
        bitcoin = M.SVGMobject("./assets/bitcoin.svg")
        bitcoin.scale_to_fit_width(0.5).to_corner(M.UL)
        euro = M.ImageMobject("./assets/euro.png")
        euro.scale_to_fit_width(0.5).next_to(separator_line).to_edge(M.UP)
        ether = M.SVGMobject("./assets/ether.svg").scale(2)

        self.play(
            M.FadeIn(*self.bitcoin_paths, *self.bank_paths,
                     *self.bitcoin_system, *self.bank_system),
            M.FadeIn(separator_line, bitcoin, euro)
        )
        self.wait()
        self.play(
            self.bitcoin_transfer_animations,
            self.bank_transfer_animations,
            run_time=10
        )
        self.wait()
        self.play(
            M.AnimationGroup(
                M.FadeOut(*self.mobjects),
                M.FadeIn(ether)
            )
        )


class SceneThree(M.Scene):
    def construct(self):
        person = M.SVGMobject("./assets/person").scale(0.5).set_color(M.WHITE)
        shannon = M.VGroup(
            M.Tex("Shannon"), person.copy().set_color(M.PINK),
        )
        wayne = M.VGroup(
            M.Tex("Wayne"), person.copy().set_color(M.BLUE),
        )

        shannon.arrange(M.UP)
        wayne.arrange(M.UP)
        M.VGroup(shannon, wayne).arrange(M.RIGHT, 5 * M.LARGE_BUFF)

        arrows = [
            M.Arrow(shannon[1].get_edge_center(M.RIGHT),
                    wayne[1].get_edge_center(M.LEFT)),
            M.Arrow(wayne[1].get_edge_center(M.LEFT),
                    shannon[1].get_edge_center(M.RIGHT))
        ]

        M.VGroup(*arrows).arrange(M.DOWN)\
            .set_color(M.LIGHTER_GRAY).set_opacity(0.2).shift(0.5 * M.UP)

        euros = M.VGroup(*[
            M.SVGMobject("./assets/euro.svg").scale(0.4)
            .next_to(person, M.UP, buff=M.LARGE_BUFF)

            for person in [shannon[1], wayne[1]]
        ])

        ethers = M.VGroup(
            *[
                M.SVGMobject("./assets/ether_coin").scale(0.4)
                .next_to(person, M.UP, buff=M.LARGE_BUFF)

                for person in [shannon[1], wayne[1]]
            ]
        )

        transactions = M.AnimationGroup(
            *my_shuffle([
                M.ShowPassingFlash(
                    M.Line(
                        arrow.get_start(),
                        arrow.get_end()
                    ).set_color(BITCOIN_YELLOW),
                    run_time=0.2
                )
                for arrow in arrows
                for _ in range(100)
            ]),
            lag_ratio=0.3
        )

        switch_to_ethereum = M.ReplacementTransform(euros, ethers)

        self.play(
            M.Create(shannon),
            M.Create(wayne),
            M.Create(M.VGroup(*arrows))
        )
        self.wait()
        self.play(M.Create(euros))
        self.wait(2)
        self.play(
            transactions,
            switch_to_ethereum,
        )
        self.wait()


class SceneFour(M.Scene):
    def construct(self):
        insurance_company = M.SVGMobject("./assets/bank.svg")\
            .set_color(M.LIGHTER_GRAY).scale(0.5)
        insurance_company_label = M.Tex("Insurance Company")

        M.VGroup(insurance_company, insurance_company_label)\
            .arrange(M.DOWN).to_edge(M.LEFT)

        person = M.SVGMobject("./assets/person.svg").scale(0.5)

        relatives = M.VGroup()
        for _ in range(3):
            relatives.add(person.copy().set_color(M.GREEN))
        relatives.arrange(center=False)

        you = person.copy().set_color(M.GREEN)
        M.VGroup(relatives, you)\
            .arrange(M.DOWN, buff=M.LARGE_BUFF * 3).to_edge(M.RIGHT)

        relatives_label = M.Tex("Your Relatives").next_to(relatives, M.UP)
        you_label = M.Tex("You").next_to(you, M.DOWN)

        cross_insurance_company = M.Cross(insurance_company)

        cash = M.ImageMobject(
            "./assets/euro.png").scale(0.5).move_to(insurance_company)
        payment_animation = []

        for i in range(len(relatives)):
            anim = M.FadeOut(
                cash.copy(), target_position=relatives[i], scale=0.1)
            payment_animation.append(anim)

        self.play(
            M.Create(insurance_company),
            M.Write(insurance_company_label),
            M.Create(M.VGroup(relatives, you)),
            M.Write(relatives_label), M.Write(you_label)
        )

        self.wait()

        self.play(M.AnimationGroup(*payment_animation))

        self.wait()

        self.play(
            M.FadeOut(you, you_label),
            M.VGroup(relatives_label, relatives)
            .animate.move_to(M.ORIGIN).to_edge(M.RIGHT),
        )

        self.wait()

        self.add(cross_insurance_company)
        self.play(M.FadeOut(cross_insurance_company,
                            insurance_company,
                            insurance_company_label),)
        self.play(
            M.VGroup(relatives_label, relatives)
            .animate.move_to(M.ORIGIN),
        )
        self.wait()


class SceneFive(M.Scene):
    def construct(self):
        title = M.Tex("Smart Contract").to_edge(M.UP)

        contract = M.Code(
            "./smart_contract.sol",
            language="Solidity",
            line_spacing=0.2,
            font_size=8,
            style="monokai"
        )

        death_certificate = M.SVGMobject("./assets/death_certificate.svg")
        death_certificate.set_color(M.WHITE).shift(3 * M.LEFT)

        beneficiaries = M.VGroup()

        for _ in range(3):
            person = M.SVGMobject(
                "./assets/person.svg").scale(0.5).set_color(M.WHITE)
            beneficiaries.add(person)
        beneficiaries.arrange(M.DOWN, buff=2 * M.LARGE_BUFF).to_edge(M.LEFT)

        ether = M.SVGMobject("./assets/ether_coin.svg").move_to(contract)
        payment_animation = []

        for i in range(len(beneficiaries)):
            anim = M.FadeOut(ether.copy(), target_position=beneficiaries[i])
            payment_animation.append(anim)

        final_message = M.Tex(
            "The contract is hardcoded and it has to be fulfilled!")

        self.play(M.Write(title))
        self.play(M.Create(contract))
        self.wait()
        self.play(contract.animate.shift(3 * M.RIGHT))
        self.wait()
        self.play(M.FadeIn(death_certificate, shift=3*M.RIGHT))
        self.wait(0.5)
        self.play(M.FadeOut(death_certificate,
                  target_position=contract, scale=0.5))
        self.play(M.FadeIn(*beneficiaries))
        self.play(M.AnimationGroup(*payment_animation))
        self.play(
            M.FadeOut(contract, shift=M.RIGHT),
            M.FadeOut(beneficiaries, shift=M.LEFT)
        )
        self.play(M.Write(final_message))
        self.wait()


class BlockChain(M.VGroup):
    def __init__(
        self,
        n=4,
        block_width=1.5,
        block_height=2,
        block_colors=[BITCOIN_YELLOW],
        chain_colors=[M.WHITE],
        **kwargs
    ):
        self.num_blocks = n
        self.block_width = block_width
        self.block_height = block_height
        self.block_colors = block_colors
        self.chain_colors = chain_colors

        self.blocks = self.initialize_blocks()
        self.chains = self.initialize_chains()

        self.blocks.set_color_by_gradient(*self.block_colors)
        self.chains.set_color_by_gradient(*self.chain_colors)

        super().__init__(**kwargs)

        self.add(self.blocks)
        self.add(self.chains)

    def initialize_blocks(self):
        blocks = []

        for _ in range(self.num_blocks):
            blocks.append(self.create_block())

        return M.VGroup(*blocks).arrange(buff=2)

    def initialize_chains(self):
        chains = []

        for i in range(self.num_blocks - 1):
            chains.append(
                self.create_chain(self.blocks[i], self.blocks[i+1])
            )

        return M.VGroup(*chains)

    def create_block(self):
        block = M.VGroup()
        block.add(M.Rectangle(width=self.block_width, height=self.block_height))
        block.add(
            M.Rectangle(width=self.block_width,
                        height=0.15 * self.block_height)
            .next_to(
                block[0],
                direction=M.ORIGIN,
                buff=0,
                aligned_edge=M.UP,
            )

        )
        block.add(
            M.Rectangle(width=self.block_width,
                        height=0.15 * self.block_height)
            .next_to(
                block[0],
                direction=M.ORIGIN,
                buff=0,
                aligned_edge=M.DOWN,
            )

        )
        return block

    def create_chain(self, currentBlock, nextBlock):
        start_point = M.interpolate(
            currentBlock.get_edge_center(M.RIGHT),
            currentBlock.get_corner(M.DR),
            0.7
        )
        target_point = M.interpolate(
            nextBlock.get_edge_center(M.LEFT),
            nextBlock.get_corner(M.UL),
            0.7
        )
        chain = M.Arrow(
            M.LEFT, M.RIGHT,
            tip_length=0.15,
        )

        chain.set_width(currentBlock.get_width())
        chain.next_to(target_point, M.LEFT, 0.5*M.SMALL_BUFF)
        chain.points[0] = start_point
        chain.points[1] = nextBlock.get_edge_center(M.LEFT)
        chain.points[2] = currentBlock.get_corner(M.UR)
        chain.points[2] = M.mid(
            currentBlock.get_edge_center(M.RIGHT),
            currentBlock.get_corner(M.UR)
        )
        return chain
        return chain
        return chain
