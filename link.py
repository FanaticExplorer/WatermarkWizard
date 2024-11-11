import customtkinter
import webbrowser


class Link(customtkinter.CTkLabel):

    def __init__(self, master=None, link=None, *args, **kwargs):
        super().__init__(master, cursor="hand2", *args, **kwargs)
        self.link = link
        self.cursor = "hand2"
        self.bind('<Button-1>', self._open_link)

    # noinspection PyUnusedLocal
    def _open_link(self, *args):
        webbrowser.open_new(self.link)


# Example usage
if __name__ == "__main__":
    root = customtkinter.CTk()
    root.geometry("400x200")

    link_label = Link(root, text="Visit Google", link="https://www.google.com")
    link_label.pack(padx=20, pady=20)

    root.mainloop()
