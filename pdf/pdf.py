import PyPDF2
from sys import argv
from pathlib import Path
from datetime import datetime
import io


def _get_output_path(fn_name: str, output_path: str) -> str | Path:
    if not output_path:
        output_path = f'{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}_{fn_name.split("_")[0]}.pdf'
    return output_path


def remove_password(input_path, password, output_path=None) -> (int, str):
    output_path = _get_output_path(remove_password.__name__, output_path)

    with open(input_path, 'rb+') as input_file, open(output_path, 'wb') as output_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        if pdf_reader.is_encrypted:
            pdf_reader.decrypt(password)

        pdf_writer = PyPDF2.PdfWriter()
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        pdf_writer.write(output_file)[1].seek(0, io.SEEK_END)

        return output_file.tell(), output_path


def compress(input_path, output_path=None) -> (int, str):
    output_path = _get_output_path(compress.__name__, output_path)

    pdf_writer = PyPDF2.PdfWriter()
    pdf_reader = PyPDF2.PdfReader(input_path)

    for page in pdf_reader.pages:
        page.compress_content_streams()
        pdf_writer.add_page(page)

    with open(output_path, 'wb+') as output_file:
        pdf_writer.write(output_file)[1].seek(0, io.SEEK_END)

        return output_file.tell(), output_path


if __name__ == "__main__":
    def main():
        if len(argv) < 1:
            print("Invalid no of arguments")
            return -1

        file_size, file_path = globals()[argv[1]](*argv[2:])

        print(f"Operation completed successfully!\nfile_size: {file_size}\nfile_path: {file_path}")

    main()

