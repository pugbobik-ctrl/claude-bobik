"""Join the per-strip PDFs from build_pdf.js into receipt/print/dinner-receipts.pdf, one strip per page."""
import pathlib
from pypdf import PdfWriter

from spec import ORDER

PRINT = pathlib.Path(__file__).parent.parent / "print"
w = PdfWriter()
for name in ORDER:
    w.append(str(PRINT / f"{name}.pdf"))
w.write(PRINT / "dinner-receipts.pdf")
print("wrote", PRINT / "dinner-receipts.pdf")
