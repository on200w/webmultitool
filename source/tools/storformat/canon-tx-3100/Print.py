from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageWin
import win32print
import win32gui
import win32ui
import win32con

hovedBilde = None
img_label = None
valgt_skriver = None
x = 914  
y = 1000  

Farge = None
Papirtype = None
Kvalitet = None
Orientering = None
AntallKopier = None

def mm_til_piksler(mm, dpi=300):
    """Convert millimeters to pixels at given DPI"""
    tommer = mm / 25.4
    return int(tommer * dpi)

def velgSkriver():
    global valgt_skriver
    skrivere = [skriver[2] for skriver in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)]
    
    if not skrivere:
        messagebox.showerror("Feil", "Ingen skrivere funnet")
        return
    
    skriver_vindu = Toplevel(root)
    skriver_vindu.title("Velg skriver")
    skriver_vindu.geometry("450x400")
    skriver_vindu.configure(bg='#f0f0f0')
    skriver_vindu.resizable(False, False)
    
    skriver_vindu.transient(root)
    skriver_vindu.grab_set()
    
    main_frame = Frame(skriver_vindu, bg='#f0f0f0')
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    title_label = Label(main_frame, text="Velg en skriver", 
                       font=("Segoe UI", 14, "bold"), 
                       bg='#f0f0f0', fg='#2c3e50')
    title_label.pack(pady=(0, 20))
    
    printer_frame = LabelFrame(main_frame, text="Tilgjengelige skrivere", 
                              font=("Segoe UI", 10), 
                              bg='#f0f0f0', fg='#2c3e50',
                              padx=15, pady=15)
    printer_frame.pack(fill=BOTH, expand=True, pady=(0, 20))
    
    skriver_var = StringVar(value=skrivere[0])
    
    for i, skriver in enumerate(skrivere):
        rb = Radiobutton(printer_frame, text=skriver, 
                        variable=skriver_var, value=skriver,
                        font=("Segoe UI", 10),
                        bg='#f0f0f0', fg='#34495e',
                        selectcolor='#3498db',
                        activebackground='#ecf0f1')
        rb.pack(anchor=W, pady=5)
    
    def velg_skriver():
        global valgt_skriver
        valgt_skriver = skriver_var.get()
        skriver_etikett.config(text=f"✓ Valgt: {valgt_skriver}", fg='#27ae60')
        skriver_vindu.destroy()
    
    button_frame = Frame(main_frame, bg='#f0f0f0')
    button_frame.pack(fill=X, pady=(10, 0))
    
    velg_btn = Button(button_frame, text="✓ Velg skriver", 
                     command=velg_skriver,
                     font=("Segoe UI", 12, "bold"),
                     bg='#2ecc71', fg='white',
                     relief=FLAT,
                     padx=25, pady=12,
                     bd=0,
                     activebackground='#27ae60',
                     activeforeground='white',
                     cursor='hand2')
    velg_btn.pack(side=RIGHT, padx=(10, 0))
    
    def on_enter_velg(e):
        velg_btn.configure(bg='#27ae60')
    
    def on_leave_velg(e):
        velg_btn.configure(bg='#2ecc71')
    
    velg_btn.bind('<Enter>', on_enter_velg)
    velg_btn.bind('<Leave>', on_leave_velg)
    
    avbryt_btn = Button(button_frame, text="✕ Avbryt", 
                       command=skriver_vindu.destroy,
                       font=("Segoe UI", 12),
                       bg='#e74c3c', fg='white',
                       relief=FLAT,
                       padx=25, pady=12,
                       bd=0,
                       activebackground='#c0392b',
                       activeforeground='white',
                       cursor='hand2')
    avbryt_btn.pack(side=RIGHT, padx=(10, 10))
    
    def on_enter_avbryt(e):
        avbryt_btn.configure(bg='#c0392b')
    
    def on_leave_avbryt(e):
        avbryt_btn.configure(bg='#e74c3c')
    
    avbryt_btn.bind('<Enter>', on_enter_avbryt)
    avbryt_btn.bind('<Leave>', on_leave_avbryt)

def avansertValg():
    global Farge, Papirtype, Kvalitet, Orientering, AntallKopier
    avansert_vindu = Toplevel(root)
    avansert_vindu.title("Avanserte utskriftsvalg")
    avansert_vindu.geometry("500x650")
    avansert_vindu.configure(bg='#f0f0f0')
    avansert_vindu.resizable(False, False)
    
    avansert_vindu.transient(root)
    avansert_vindu.grab_set()

    main_container = Frame(avansert_vindu, bg='#f0f0f0')
    main_container.pack(fill=BOTH, expand=True, padx=25, pady=25)
    
    title_label = Label(main_container, text="Avanserte utskriftsvalg", 
                       font=("Segoe UI", 16, "bold"), 
                       bg='#f0f0f0', fg='#2c3e50')
    title_label.pack(pady=(0, 30))

    settings_frame = Frame(main_container, bg='#f0f0f0')
    settings_frame.pack(fill=BOTH, expand=True)

    color_frame = LabelFrame(settings_frame, text="Fargealternativer", 
                            font=("Segoe UI", 11, "bold"),
                            bg='#f0f0f0', fg='#2c3e50',
                            padx=20, pady=15)
    color_frame.pack(fill=X, pady=(0, 15))
    
    farge_var = StringVar(value=Farge.get() if Farge else "Farge")
    farge_combo = ttk.Combobox(color_frame, textvariable=farge_var,
                              values=["Farge", "Svart-hvitt"],
                              state="readonly", font=("Segoe UI", 10))
    farge_combo.pack(fill=X)

    paper_frame = LabelFrame(settings_frame, text="Papirtype", 
                           font=("Segoe UI", 11, "bold"),
                           bg='#f0f0f0', fg='#2c3e50',
                           padx=20, pady=15)
    paper_frame.pack(fill=X, pady=(0, 15))
    
    papir_var = StringVar(value=Papirtype if Papirtype else "Normalt papir")
    papir_combo = ttk.Combobox(paper_frame, textvariable=papir_var,
                              values=["Normalt papir", "Fotopapir", "Matt papir", "Glossy papir"],
                              state="readonly", font=("Segoe UI", 10))
    papir_combo.pack(fill=X)

    quality_frame = LabelFrame(settings_frame, text="Utskriftskvalitet", 
                             font=("Segoe UI", 11, "bold"),
                             bg='#f0f0f0', fg='#2c3e50',
                             padx=20, pady=15)
    quality_frame.pack(fill=X, pady=(0, 15))
    
    kvalitet_var = StringVar(value=Kvalitet if Kvalitet else "Normal")
    kvalitet_combo = ttk.Combobox(quality_frame, textvariable=kvalitet_var,
                                 values=["Lav", "Normal", "Høy", "Beste"],
                                 state="readonly", font=("Segoe UI", 10))
    kvalitet_combo.pack(fill=X)

    orient_frame = LabelFrame(settings_frame, text="Orientering", 
                            font=("Segoe UI", 11, "bold"),
                            bg='#f0f0f0', fg='#2c3e50',
                            padx=20, pady=15)
    orient_frame.pack(fill=X, pady=(0, 15))
    
    orientering_var = StringVar(value=Orientering if Orientering else "Portrett")
    orientering_combo = ttk.Combobox(orient_frame, textvariable=orientering_var,
                                   values=["Portrett", "Landskap"],
                                   state="readonly", font=("Segoe UI", 10))
    orientering_combo.pack(fill=X)

    copies_frame = LabelFrame(settings_frame, text="Antall kopier", 
                            font=("Segoe UI", 11, "bold"),
                            bg='#f0f0f0', fg='#2c3e50',
                            padx=20, pady=15)
    copies_frame.pack(fill=X, pady=(0, 20))
    
    kopier_var = StringVar(value=str(AntallKopier) if AntallKopier else "1")
    kopier_spinbox = Spinbox(copies_frame, from_=1, to=10, textvariable=kopier_var, 
                           width=10, font=("Segoe UI", 10))
    kopier_spinbox.pack(anchor=W)

    def lagre_avanserte_valg():
        global Farge, Papirtype, Kvalitet, Orientering, AntallKopier
        Farge.set(farge_var.get())
        Papirtype = papir_var.get()
        Kvalitet = kvalitet_var.get()
        Orientering = orientering_var.get()
        AntallKopier = int(kopier_var.get())
        avansert_vindu.destroy()

    button_frame = Frame(main_container, bg='#f0f0f0')
    button_frame.pack(fill=X, pady=(20, 0))
    
    lagre_btn = Button(button_frame, text="✓ Lagre og lukk", 
                      command=lagre_avanserte_valg,
                      font=("Segoe UI", 12, "bold"),
                      bg='#2ecc71', fg='white',
                      relief=FLAT,
                      padx=25, pady=12,
                      bd=0,
                      activebackground='#27ae60',
                      activeforeground='white',
                      cursor='hand2')
    lagre_btn.pack(side=RIGHT, padx=(10, 0))
    
    def on_enter_lagre(e):
        lagre_btn.configure(bg='#27ae60')
    
    def on_leave_lagre(e):
        lagre_btn.configure(bg='#2ecc71')
    
    lagre_btn.bind('<Enter>', on_enter_lagre)
    lagre_btn.bind('<Leave>', on_leave_lagre)
    
    avbryt_btn = Button(button_frame, text="✕ Avbryt", 
                       command=avansert_vindu.destroy,
                       font=("Segoe UI", 12),
                       bg='#e74c3c', fg='white',
                       relief=FLAT,
                       padx=25, pady=12,
                       bd=0,
                       activebackground='#c0392b',
                       activeforeground='white',
                       cursor='hand2')
    avbryt_btn.pack(side=RIGHT, padx=(10, 10))
    
    def on_enter_avbryt(e):
        avbryt_btn.configure(bg='#c0392b')
    
    def on_leave_avbryt(e):
        avbryt_btn.configure(bg='#e74c3c')
    
    avbryt_btn.bind('<Enter>', on_enter_avbryt)
    avbryt_btn.bind('<Leave>', on_leave_avbryt)

def lastOppFunksjon():
    global hovedBilde, img_label
    filsti = filedialog.askopenfilename(
        title="Velg en bildefil",
        filetypes=(
            ("Bildefiler", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.ico"),
            ("Alle filer", "*.*")
        )
    )
    if filsti:
        try:
            img = Image.open(filsti)
            print(f"Bilde valgt: {filsti}")
            
            filename = filsti.split('/')[-1]
            file_path_label.config(text=f"📁 {filename}", fg='#27ae60')
            
            display_img = img.copy()
            max_width, max_height = 300, 300
            display_img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(display_img)
            
            if img_label:
                img_label.destroy()
            
            for widget in preview_frame.winfo_children():
                if isinstance(widget, Label) and widget != img_label:
                    widget.destroy()
            
            img_label = Label(preview_frame, image=photo, bg='white', 
                            relief=SOLID, borderwidth=1)
            img_label.image = photo  
            img_label.pack(pady=10)
            
            original_size_label = Label(preview_frame, 
                                      text=f"Original størrelse: {img.width} x {img.height} piksler",
                                      font=("Segoe UI", 9),
                                      bg='#f5f5f5', fg='#7f8c8d')
            original_size_label.pack(pady=(0, 5))
            
            hovedBilde = img
            
            preview_frame.update_idletasks()
            
        except Exception as e:
            print(f"Feil ved åpning av bilde: {e}")
            messagebox.showerror("Feil", f"Kunne ikke åpne bildefilen:\n{e}")
    else:
        print("Ingen bilde valgt.")

def skrivUtBilde():
    global hovedBilde, valgt_skriver
    if not hovedBilde:
        messagebox.showerror("Feil", "Ingen bilde valgt")
        return
    
    if not valgt_skriver:
        messagebox.showerror("Feil", "Ingen skriver valgt")
        return
    
    try:
        bredde_mm = int(x_entry.get())
        hoyde_mm = int(y_entry.get())

        bredde_px = mm_til_piksler(bredde_mm)
        hoyde_px = mm_til_piksler(hoyde_mm)

        endret_img = hovedBilde.resize((bredde_px, hoyde_px), Image.Resampling.LANCZOS)
        
        if Farge and Farge.get() == "Svart-hvitt":
            endret_img = endret_img.convert('L')

        avansert_info = f"Farge: {Farge.get() if Farge else 'Farge'}\nPapirtype: {Papirtype}\nKvalitet: {Kvalitet}\nOrientering: {Orientering}\nAntall kopier: {AntallKopier}"

        try:
            pHandle = win32print.OpenPrinter(valgt_skriver)
            try:
                pInfo = win32print.GetPrinter(pHandle, 2)
                pDevMode = pInfo["pDevMode"]
                
                if pDevMode:
                    if Orientering == "Landskap":
                        pDevMode.Orientation = 2 
                    else:
                        pDevMode.Orientation = 1  
                    
                    if Farge and Farge.get() == "Svart-hvitt":
                        pDevMode.Color = 1  
                    else:
                        pDevMode.Color = 2  
                    
                    quality_map = {
                        "Lav": -1,      
                        "Normal": -2,    
                        "Høy": -3,      
                        "Beste": -4     
                    }
                    if Kvalitet in quality_map:
                        pDevMode.PrintQuality = quality_map[Kvalitet]
                    
                    if Papirtype and "foto" in Papirtype.lower():
                        try:
                            pDevMode.MediaType = 1
                        except AttributeError:
                            pass
                    
                    if AntallKopier:
                        pDevMode.Copies = AntallKopier

                    pDevMode.PaperSize = 0
                    pDevMode.PaperWidth = int(bredde_mm * 10)
                    pDevMode.PaperLength = int(hoyde_mm * 10)
                    DM_PAPERLENGTH = 0x00000004
                    DM_PAPERWIDTH = 0x00000008
                    if hasattr(pDevMode, 'Fields'):
                        pDevMode.Fields |= DM_PAPERLENGTH | DM_PAPERWIDTH
                    elif hasattr(pDevMode, 'dmFields'):
                        pDevMode.dmFields |= DM_PAPERLENGTH | DM_PAPERWIDTH

                    pInfo["pDevMode"] = pDevMode
                    win32print.SetPrinter(pHandle, 2, pInfo, 0)
            finally:
                win32print.ClosePrinter(pHandle)
        except Exception as devmode_error:
            print(f"Warning: Could not configure advanced printer settings: {devmode_error}")

        hDC = win32gui.CreateDC("WINSPOOL", valgt_skriver, None)
        hdc = win32ui.CreateDCFromHandle(hDC)

        page_width = hdc.GetDeviceCaps(win32con.HORZRES)
        page_height = hdc.GetDeviceCaps(win32con.VERTRES)
        
        printer_dpi_x = hdc.GetDeviceCaps(win32con.LOGPIXELSX)
        printer_dpi_y = hdc.GetDeviceCaps(win32con.LOGPIXELSY)
        
        print_width_units = int((bredde_mm / 25.4) * printer_dpi_x)
        print_height_units = int((hoyde_mm / 25.4) * printer_dpi_y)

        if Orientering == "Landskap":
            print_width_units, print_height_units = print_height_units, print_width_units

        hdc.StartDoc("Utskrift av bilde")
        num_copies = AntallKopier if AntallKopier else 1
        for i in range(num_copies):
            hdc.StartPage()
            dib = ImageWin.Dib(endret_img)
            dib.draw(hdc.GetHandleOutput(), (0, 0, print_width_units, print_height_units))
            hdc.EndPage()
        hdc.EndDoc()
        hdc.DeleteDC()

        messagebox.showinfo("Suksess", f"Bilde sendt til skriver\n\n{avansert_info}")

    except ValueError:
        messagebox.showerror("Feil", "Vennligst skriv inn gyldige tall for bredde og høyde")
    except Exception as e:
        messagebox.showerror("Feil", f"Feil ved utskrift av bilde: {e}")

def main():
    global root, x_entry, y_entry, img_label, skriver_etikett, Farge, Papirtype, Kvalitet, Orientering, AntallKopier
    global file_path_label, preview_frame
    
    root = Tk()
    root.title("Bildeprinter - Profesjonell utskrift")
    root.geometry("800x900")
    root.configure(bg='#f5f5f5')
    root.resizable(True, True) 

    Farge = StringVar(value="Farge")
    Papirtype = "Normalt papir"
    Kvalitet = "Normal"
    Orientering = "Portrett"
    AntallKopier = 1

    main_frame = Frame(root, bg='#f5f5f5')
    main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    canvas = Canvas(main_frame, bg='#f5f5f5', highlightthickness=0)
    scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = Frame(canvas, bg='#f5f5f5')
    
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        canvas_height = canvas.winfo_height()
        content_height = scrollable_frame.winfo_reqheight()
        if content_height > canvas_height and hasattr(root, 'scroll_hint'):
            root.scroll_hint.pack(side=BOTTOM, fill=X)
        elif hasattr(root, 'scroll_hint'):
            root.scroll_hint.pack_forget()
        
        canvas_width = canvas.winfo_width()
        frame_width = scrollable_frame.winfo_reqwidth()
        
        if frame_width < canvas_width and canvas.find_all():
            x_offset = (canvas_width - frame_width) // 2
            canvas.coords(canvas.find_all()[0], x_offset, 0)
    
    scrollable_frame.bind("<Configure>", on_frame_configure)
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        canvas_width = canvas.winfo_width()
        frame_width = scrollable_frame.winfo_reqwidth()
        
        if frame_width < canvas_width:
            x_offset = (canvas_width - frame_width) // 2
            canvas.coords(canvas.find_all()[0], x_offset, 0)
        else:
            canvas.coords(canvas.find_all()[0], 0, 0)
    
    canvas.bind("<Configure>", on_canvas_configure)
    
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _on_key_scroll(event):
        if event.keysym == 'Up':
            canvas.yview_scroll(-1, "units")
        elif event.keysym == 'Down':
            canvas.yview_scroll(1, "units")
        elif event.keysym == 'Page_Up':
            canvas.yview_scroll(-5, "units")
        elif event.keysym == 'Page_Down':
            canvas.yview_scroll(5, "units")
        elif event.keysym == 'Home':
            canvas.yview_moveto(0)
        elif event.keysym == 'End':
            canvas.yview_moveto(1)
    
    root.bind('<Key>', _on_key_scroll)
    root.focus_set() 
    
    root.scroll_hint = Label(root, text="↕ Du kan bla opp og ned med musehjulet, piltastene eller Page Up/Down",
                            font=("Segoe UI", 8), bg='#ecf0f1', fg='#7f8c8d', 
                            relief=FLAT, pady=2)

    main_container = Frame(scrollable_frame, bg='#f5f5f5')
    main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)

    title_label = Label(main_container, text="📖 Bildeprinter", 
                       font=("Segoe UI", 24, "bold"), 
                       bg='#f5f5f5', fg='#2c3e50')
    title_label.pack(pady=(0, 30))

    file_section = LabelFrame(main_container, text="1. Velg bildefil", 
                             font=("Segoe UI", 14, "bold"),
                             bg='#f5f5f5', fg='#2c3e50',
                             padx=25, pady=20)
    file_section.pack(fill=X, pady=(0, 20))

    file_button_frame = Frame(file_section, bg='#f5f5f5')
    file_button_frame.pack(fill=X, pady=(0, 10))

    upload_btn = Button(file_button_frame, text="📁 Last opp bilde", 
                       command=lastOppFunksjon,
                       font=("Segoe UI", 12, "bold"),
                       bg='#3498db', fg='white',
                       relief=FLAT, padx=25, pady=12,
                       cursor='hand2')
    upload_btn.pack(side=LEFT)

    file_path_label = Label(file_button_frame, text="Ingen fil valgt", 
                          font=("Segoe UI", 11), 
                          bg='#f5f5f5', fg='#7f8c8d')
    file_path_label.pack(side=LEFT, padx=(20, 0))

    preview_frame = Frame(file_section, bg='#f5f5f5')
    preview_frame.pack(fill=X, pady=(10, 0))

    printer_section = LabelFrame(main_container, text="2. Velg skriver", 
                                font=("Segoe UI", 14, "bold"),
                                bg='#f5f5f5', fg='#2c3e50',
                                padx=25, pady=20)
    printer_section.pack(fill=X, pady=(0, 20))

    printer_button_frame = Frame(printer_section, bg='#f5f5f5')
    printer_button_frame.pack(fill=X, pady=(0, 10))

    printer_btn = Button(printer_button_frame, text="🖨️ Velg skriver", 
                        command=velgSkriver,
                        font=("Segoe UI", 12, "bold"),
                        bg='#e67e22', fg='white',
                        relief=FLAT, padx=25, pady=12,
                        cursor='hand2')
    printer_btn.pack(side=LEFT)

    skriver_etikett = Label(printer_button_frame, text="Ingen skriver valgt", 
                          font=("Segoe UI", 11), 
                          bg='#f5f5f5', fg='#7f8c8d')
    skriver_etikett.pack(side=LEFT, padx=(20, 0))

    advanced_btn = Button(printer_button_frame, text="⚙️ Avanserte valg", 
                         command=avansertValg,
                         font=("Segoe UI", 11),
                         bg='#9b59b6', fg='white',
                         relief=FLAT, padx=20, pady=8,
                         cursor='hand2')
    advanced_btn.pack(side=RIGHT)

    dimensions_section = LabelFrame(main_container, text="3. Angi dimensjoner", 
                                   font=("Segoe UI", 14, "bold"),
                                   bg='#f5f5f5', fg='#2c3e50',
                                   padx=25, pady=20)
    dimensions_section.pack(fill=X, pady=(0, 20))

    dimensions_frame = Frame(dimensions_section, bg='#f5f5f5')
    dimensions_frame.pack(fill=X)

    width_frame = Frame(dimensions_frame, bg='#f5f5f5')
    width_frame.pack(side=LEFT, expand=True, fill=X)

    width_label = Label(width_frame, text="Bredde (mm):", 
                       font=("Segoe UI", 11, "bold"), 
                       bg='#f5f5f5', fg='#2c3e50')
    width_label.pack(anchor=W, pady=(0, 5))

    x_entry = Entry(width_frame, font=("Segoe UI", 12), width=15,
                   relief=SOLID, borderwidth=1)
    x_entry.insert(0, str(x))
    x_entry.pack(anchor=W)

    spacer = Frame(dimensions_frame, bg='#f5f5f5', width=30)
    spacer.pack(side=LEFT)

    height_frame = Frame(dimensions_frame, bg='#f5f5f5')
    height_frame.pack(side=LEFT, expand=True, fill=X)

    height_label = Label(height_frame, text="Høyde (mm):", 
                        font=("Segoe UI", 11, "bold"), 
                        bg='#f5f5f5', fg='#2c3e50')
    height_label.pack(anchor=W, pady=(0, 5))

    y_entry = Entry(height_frame, font=("Segoe UI", 12), width=15,
                   relief=SOLID, borderwidth=1)
    y_entry.insert(0, str(y))
    y_entry.pack(anchor=W)

    print_section = Frame(main_container, bg='#f5f5f5')
    print_section.pack(fill=X, pady=(20, 0))

    print_btn = Button(print_section, text="🖨️ Skriv ut", 
                      command=skrivUtBilde,
                      font=("Segoe UI", 16, "bold"),
                      bg='#27ae60', fg='white',
                      relief=FLAT, padx=40, pady=15,
                      cursor='hand2')
    print_btn.pack()

    def on_enter(e):
        e.widget.configure(bg=e.widget.cget('bg'))
        
    def on_leave(e):
        e.widget.configure(bg=e.widget.cget('bg'))

    root.focus_force()
    
    root.mainloop()

if __name__ == "__main__":
    main()