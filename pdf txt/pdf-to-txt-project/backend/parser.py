import pdfplumber
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def convert_pdf_to_txt(pdf_path, txt_path):
    """
    将PDF文件转换为TXT文件。

    参数:
        pdf_path (str): PDF文件的路径
        txt_path (str): 输出TXT文件的路径

    返回:
        bool: 转换成功返回True，否则返回False
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_content = []

            # 遍历每一页提取文本
            for page_num, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    text_content.append(f"=== Page {page_num} ===\n")
                    text_content.append(page_text)
                    text_content.append("\n")  # 添加空行分隔页
                else:
                    # 如果提取不到文本，可能是扫描件或空页
                    logger.warning(f"Page {page_num} has no extractable text.")
                    text_content.append(f"=== Page {page_num} ===\n")
                    text_content.append("[No text content]\n")

            # 如果没有提取到任何文本
            if not text_content:
                logger.error("No text could be extracted from the PDF.")
                return False

            # 将文本写入TXT文件
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(''.join(text_content))

            logger.info(f"Successfully converted {pdf_path} to {txt_path}")
            return True

    except pdfplumber.exceptions.PDFSyntaxError as e:
        logger.error(f"Invalid PDF file: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during conversion: {e}")
        return False

# 如果直接运行此脚本，可以测试转换功能
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python parser.py <input_pdf> <output_txt>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_txt = sys.argv[2]
    success = convert_pdf_to_txt(input_pdf, output_txt)
    if success:
        print("Conversion successful!")
    else:
        print("Conversion failed!")
        sys.exit(1)