
from core.generator import TextGenerator, TextForgeError

def main():

    print("\nTEXTFORGE AI - MOTOR GENERATIVO")
    print("=" * 50)

    try:

        generator = TextGenerator()

        prompt = (
            "Explique o conceito de Machine Learning "
            "e apresente três aplicações práticas."
        )

        print("\nGerando conteúdo...\n")

        response = generator.generate(
            prompt=prompt,
            temperature=0.7,
            max_tokens=2048
        )

        print("RESPOSTA GERADA")
        print("-" * 50)
        print(response)

        print("\n" + "=" * 50)
        print("Motor generativo funcionando!")

    except TextForgeError as error:
        print(f"\nErro do TextForge: {error}")

    except Exception as error:
        print(f"\nErro inesperado: {error}")


if __name__ == "__main__":
    main()
