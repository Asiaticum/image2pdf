import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog
from tkinter import messagebox
import os
import img2pdf


class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("画像ファイルをPDFに変換")

        # ウィンドウのサイズを設定
        self.root.geometry("600x300")

        # ドラッグ&ドロップエリア
        self.drop_area = tk.Label(
            root,
            text="ここにファイル・フォルダをドラッグ&ドロップしてください\nまたはボタンをクリックしてファイル・フォルダを選択してください",
            width=100,
            height=14,
        )
        self.drop_area.pack(pady=10)

        # ドラッグ&ドロップの設定
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind("<<Drop>>", self.on_drop)

        # ボタンを配置するためのフレーム
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        # ファイル選択ボタン
        self.select_file_button = tk.Button(
            self.button_frame, text="ファイルを選択", command=self.select_file
        )
        self.select_file_button.grid(row=0, column=0, padx=5)

        # ファイル・フォルダ選択ボタン
        self.select_folder_button = tk.Button(
            self.button_frame, text="フォルダを選択", command=self.select_folder
        )
        self.select_folder_button.grid(row=0, column=1, padx=5)

    def on_drop(self, event):
        item_path = event.data
        if item_path.endswith("}"):
            item_path = item_path[1:][:-1]
        if os.path.isdir(item_path):
            self.convert_images_to_pdf(item_path)
        elif os.path.isfile(item_path) and any(
            item_path.endswith(ext)
            for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]
        ):
            self.convert_image_file_to_pdf(item_path)
        else:
            messagebox.showinfo(
                "エラー", "画像ファイルまたはフォルダをドロップしてください。"
            )

    def select_folder(self):
        # フォルダ選択ダイアログの設定を変更して、フォルダ選択を許可
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.convert_images_to_pdf(folder_path)

    def select_file(self):
        # ファイル選択ダイアログの設定を変更して、ファイル選択を許可
        item_path = filedialog.askopenfilename()
        if item_path and any(
            item_path.endswith(ext)
            for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]
        ):
            self.convert_image_file_to_pdf(item_path)

    def convert_image_file_to_pdf(self, image_file):
        file_name, _ = os.path.splitext(image_file)
        output_pdf_path = os.path.join(
            os.path.dirname(image_file), os.path.basename(file_name) + ".pdf"
        )

        try:
            with open(output_pdf_path, "wb") as f:
                f.write(img2pdf.convert(image_file))
            messagebox.showinfo(
                "成功", "PDFファイルが作成されました。\n" + output_pdf_path
            )
        except Exception as e:
            messagebox.showerror("エラー", str(e))

    def convert_images_to_pdf(self, folder_path):
        extensions = [".png", ".jpg", ".jpeg"]
        image_files = [
            os.path.join(folder_path, j)
            for j in os.listdir(folder_path)
            if any(j.endswith(ext) for ext in extensions)
        ]

        if not image_files:
            messagebox.showinfo("結果", "対象の画像ファイルが見つかりませんでした。")
            return

        # 画像ファイルを作成日時でソート
        sorted_images = sorted(image_files, key=lambda x: os.path.getctime(x))

        output_pdf_path = os.path.join(folder_path, "output.pdf")

        try:
            with open(output_pdf_path, "wb") as f:
                f.write(img2pdf.convert([image_path for image_path in sorted_images]))
            messagebox.showinfo(
                "成功", "PDFファイルが作成されました。\n" + output_pdf_path
            )
        except Exception as e:
            messagebox.showerror("エラー", str(e))


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()
