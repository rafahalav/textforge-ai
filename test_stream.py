
from core.generator import TextGenerator, TextForgeError


def main():

    print("\nTEXTFORGE AI - STREAMING")
    print("=" * 50)

    try:

        generator = TextGenerator()

        prompt = (
            "Escreva um pequeno texto sobre "
            "o futuro da inteligência artificial."
        )

        print("\nResposta da IA:\n")

        for fragment in generator.stream(
            prompt=prompt,
            temperature=0.7,
            max_tokens=2048
        ):
            print(fragment, end="", flush=True)

        print("\n\nStreaming finalizado!")

    except TextForgeError as error:
        print(f"\nErro do TextForge: {error}")

    except Exception as error:
        print(f"\nErro inesperado: {error}")


if __name__ == "__main__":
    main()
