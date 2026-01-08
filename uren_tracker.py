import customtkinter as ctk
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "uren_data.json"

COLORS = {
    'bg': '#0f0f0f',
    'card': '#1a1a1a',
    'accent': '#2d2d2d',
    'purple': '#a855f7',
    'green': '#22c55e',
    'red': '#ef4444',
    'orange': '#f97316',
    'text': '#ffffff',
    'text_dim': '#737373'
}

def laad_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    return {
        "maand_doel_uren": 152,
        "uurloon": 25,
        "bruto_totaal": 3800,
        "netto_totaal": 2217.87,
        "gewerkte_dagen": [
            {"datum": "13-12-2025", "uren": 4.5, "notitie": "Za"},
            {"datum": "14-12-2025", "uren": 4.5, "notitie": "Zo"},
            {"datum": "15-12-2025", "uren": 4, "notitie": "Ma"},
            {"datum": "17-12-2025", "uren": 2, "notitie": "Wo"},
            {"datum": "18-12-2025", "uren": 3.5, "notitie": "Do"},
            {"datum": "19-12-2025", "uren": 5, "notitie": "Vr"},
            {"datum": "20-12-2025", "uren": 4, "notitie": "Za"},
            {"datum": "21-12-2025", "uren": 4, "notitie": "Zo"},
            {"datum": "22-12-2025", "uren": 2, "notitie": "Ma"},
            {"datum": "23-12-2025", "uren": 3, "notitie": "Di"},
            {"datum": "24-12-2025", "uren": 5, "notitie": "Wo"},
            {"datum": "26-12-2025", "uren": 1.5, "notitie": "Vr"},
            {"datum": "27-12-2025", "uren": 4, "notitie": "Za"},
            {"datum": "28-12-2025", "uren": 4, "notitie": "Zo"},
            {"datum": "29-12-2025", "uren": 3.5, "notitie": "Ma"},
            {"datum": "30-12-2025", "uren": 7, "notitie": "Di"},
            {"datum": "01-01-2026", "uren": 4, "notitie": "Do"},
            {"datum": "02-01-2026", "uren": 8, "notitie": "Vr"}
        ],
        "uitgaven_broertje": [
            {"datum": "13-12-2025", "bedrag": 50, "omschrijving": ""},
            {"datum": "15-12-2025", "bedrag": 20, "omschrijving": ""},
            {"datum": "19-12-2025", "bedrag": 30, "omschrijving": ""},
            {"datum": "21-12-2025", "bedrag": 27, "omschrijving": ""},
            {"datum": "27-12-2025", "bedrag": 30, "omschrijving": ""},
            {"datum": "30-12-2025", "bedrag": 20, "omschrijving": ""},
            {"datum": "02-01-2026", "bedrag": 120, "omschrijving": ""}
        ]
    }

def sla_data_op(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

class UrenTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Uren Tracker")
        self.geometry("1000x750")
        self.minsize(800, 600)

        ctk.set_appearance_mode("dark")
        self.configure(fg_color=COLORS['bg'])

        self.data = laad_data()
        self.create_ui()
        self.update_alles()

    def create_ui(self):
        self.main = ctk.CTkScrollableFrame(self, fg_color=COLORS['bg'])
        self.main.pack(fill="both", expand=True, padx=30, pady=20)

        # Header
        ctk.CTkLabel(
            self.main, text="Uren Tracker",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COLORS['text']
        ).pack(anchor="w", pady=(0, 20))

        # === TOP STATS ===
        stats = ctk.CTkFrame(self.main, fg_color="transparent")
        stats.pack(fill="x", pady=(0, 20))

        self.card1 = self.make_card(stats, "GEWERKT", "0", "uur", COLORS['green'])
        self.card1.pack(side="left", fill="both", expand=True, padx=(0, 8))

        self.card2 = self.make_card(stats, "NOG TE WERKEN", "0", "uur", COLORS['orange'])
        self.card2.pack(side="left", fill="both", expand=True, padx=8)

        self.card3 = self.make_card(stats, "TERUG AAN VADER", "€0", "", COLORS['red'])
        self.card3.pack(side="left", fill="both", expand=True, padx=8)

        self.card4 = self.make_card(stats, "JIJ HOUDT OVER", "€0", "", COLORS['purple'])
        self.card4.pack(side="left", fill="both", expand=True, padx=(8, 0))

        # === UREN OVERZICHT ===
        uren_box = ctk.CTkFrame(self.main, fg_color=COLORS['card'], corner_radius=12)
        uren_box.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(uren_box, text="Uren Overzicht", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(12, 8))

        grid = ctk.CTkFrame(uren_box, fg_color="transparent")
        grid.pack(fill="x", padx=15, pady=(0, 12))

        left = ctk.CTkFrame(grid, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True)

        right = ctk.CTkFrame(grid, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        self.row_doel = self.make_row(left, "Doel", "152 uur")
        self.row_gewerkt = self.make_row(left, "Gewerkt", "0 uur", COLORS['green'])
        self.row_uitgaven_uren = self.make_row(left, "Uitgaven (telt als uren)", "+0 uur", COLORS['green'])

        self.row_totaal_gedaan = self.make_row(right, "Totaal gedaan", "0 uur", COLORS['green'])
        self.row_nog = self.make_row(right, "Nog te werken", "0 uur", COLORS['orange'])
        self.row_uitgaven_geld = self.make_row(right, "Uitgaven broertje", "€0", COLORS['text_dim'])

        # === GELD OVERZICHT ===
        geld_box = ctk.CTkFrame(self.main, fg_color=COLORS['card'], corner_radius=12)
        geld_box.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(geld_box, text="Geld", font=ctk.CTkFont(size=15, weight="bold")).pack(anchor="w", padx=15, pady=(12, 8))

        geld_grid = ctk.CTkFrame(geld_box, fg_color="transparent")
        geld_grid.pack(fill="x", padx=15, pady=(0, 12))

        geld_left = ctk.CTkFrame(geld_grid, fg_color="transparent")
        geld_left.pack(side="left", fill="both", expand=True)

        geld_right = ctk.CTkFrame(geld_grid, fg_color="transparent")
        geld_right.pack(side="left", fill="both", expand=True)

        self.row_bruto = self.make_row(geld_left, "Bruto (152 uur)", "€3.800")
        self.row_netto = self.make_row(geld_left, "Netto (152 uur)", "€2.218", COLORS['green'])

        self.row_nu_verdiend = self.make_row(geld_right, "Nu verdiend", "€0", COLORS['green'])
        self.row_terug = self.make_row(geld_right, "Terug aan vader", "€0", COLORS['red'])
        self.row_over = self.make_row(geld_right, "Jij houdt over", "€0", COLORS['purple'])

        # === TABS ===
        self.tabs = ctk.CTkTabview(
            self.main, fg_color=COLORS['card'],
            segmented_button_fg_color=COLORS['accent'],
            segmented_button_selected_color=COLORS['purple'],
            segmented_button_unselected_color=COLORS['accent'],
            corner_radius=12
        )
        self.tabs.pack(fill="both", expand=True)

        self.tab1 = self.tabs.add("Uren")
        self.tab2 = self.tabs.add("Uitgaven")
        self.tab3 = self.tabs.add("Instellingen")

        self.make_uren_tab()
        self.make_uitgaven_tab()
        self.make_settings_tab()

    def make_card(self, parent, title, value, suffix, color):
        card = ctk.CTkFrame(parent, fg_color=COLORS['card'], corner_radius=12, height=100)
        card.pack_propagate(False)

        bar = ctk.CTkFrame(card, fg_color=color, height=3, corner_radius=2)
        bar.pack(fill="x", padx=15, pady=(12, 8))

        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=10, weight="bold"), text_color=COLORS['text_dim']).pack(anchor="w", padx=15)

        val_frame = ctk.CTkFrame(card, fg_color="transparent")
        val_frame.pack(anchor="w", padx=15)

        lbl = ctk.CTkLabel(val_frame, text=value, font=ctk.CTkFont(size=28, weight="bold"), text_color=color)
        lbl.pack(side="left")

        if suffix:
            ctk.CTkLabel(val_frame, text=f" {suffix}", font=ctk.CTkFont(size=14), text_color=COLORS['text_dim']).pack(side="left", pady=(6, 0))

        card.lbl = lbl
        return card

    def make_row(self, parent, label, value, color=None):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=3)

        ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=12), text_color=COLORS['text_dim']).pack(side="left")

        lbl = ctk.CTkLabel(row, text=value, font=ctk.CTkFont(size=12, weight="bold"), text_color=color or COLORS['text'])
        lbl.pack(side="right")

        return lbl

    def make_uren_tab(self):
        inp = ctk.CTkFrame(self.tab1, fg_color="transparent")
        inp.pack(fill="x", pady=(5, 12))

        ctk.CTkLabel(inp, text="Datum", text_color=COLORS['text_dim']).pack(side="left", padx=(0, 5))
        wrap = ctk.CTkFrame(inp, fg_color="white", corner_radius=6)
        wrap.pack(side="left", padx=(0, 12))
        self.date1 = DateEntry(wrap, width=10, date_pattern='dd-mm-yyyy', font=('Segoe UI', 9))
        self.date1.pack(padx=2, pady=2)

        ctk.CTkLabel(inp, text="Uren", text_color=COLORS['text_dim']).pack(side="left", padx=(0, 5))
        self.uren_inp = ctk.CTkEntry(inp, width=50, fg_color=COLORS['accent'], border_width=0)
        self.uren_inp.pack(side="left", padx=(0, 12))

        ctk.CTkLabel(inp, text="Notitie", text_color=COLORS['text_dim']).pack(side="left", padx=(0, 5))
        self.notitie_inp = ctk.CTkEntry(inp, width=100, fg_color=COLORS['accent'], border_width=0)
        self.notitie_inp.pack(side="left", padx=(0, 12))

        ctk.CTkButton(inp, text="Toevoegen", command=self.add_uren, fg_color=COLORS['green'], hover_color="#16a34a", width=90, corner_radius=6).pack(side="left", padx=(0, 6))
        ctk.CTkButton(inp, text="Verwijder", command=self.del_uren, fg_color=COLORS['red'], hover_color="#dc2626", width=70, corner_radius=6).pack(side="left")

        tree_wrap = ctk.CTkFrame(self.tab1, fg_color=COLORS['accent'], corner_radius=10)
        tree_wrap.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('T.Treeview', background=COLORS['accent'], foreground='white', fieldbackground=COLORS['accent'], font=('Segoe UI', 10), rowheight=28)
        style.configure('T.Treeview.Heading', font=('Segoe UI', 10, 'bold'), background=COLORS['purple'], foreground='white')
        style.map('T.Treeview', background=[('selected', COLORS['purple'])])

        self.tree1 = ttk.Treeview(tree_wrap, columns=('datum', 'dag', 'uren', 'notitie'), show='headings', style='T.Treeview', height=8)
        self.tree1.heading('datum', text='Datum')
        self.tree1.heading('dag', text='Dag')
        self.tree1.heading('uren', text='Uren')
        self.tree1.heading('notitie', text='Notitie')
        self.tree1.column('datum', width=90, anchor='center')
        self.tree1.column('dag', width=50, anchor='center')
        self.tree1.column('uren', width=60, anchor='center')
        self.tree1.column('notitie', width=120)

        scroll = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.tree1.yview)
        self.tree1.configure(yscrollcommand=scroll.set)
        self.tree1.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scroll.pack(side="right", fill="y", pady=8, padx=(0, 8))

    def make_uitgaven_tab(self):
        inp = ctk.CTkFrame(self.tab2, fg_color="transparent")
        inp.pack(fill="x", pady=(5, 12))

        ctk.CTkLabel(inp, text="Datum", text_color=COLORS['text_dim']).pack(side="left", padx=(0, 5))
        wrap = ctk.CTkFrame(inp, fg_color="white", corner_radius=6)
        wrap.pack(side="left", padx=(0, 12))
        self.date2 = DateEntry(wrap, width=10, date_pattern='dd-mm-yyyy', font=('Segoe UI', 9))
        self.date2.pack(padx=2, pady=2)

        ctk.CTkLabel(inp, text="Bedrag €", text_color=COLORS['text_dim']).pack(side="left", padx=(0, 5))
        self.bedrag_inp = ctk.CTkEntry(inp, width=60, fg_color=COLORS['accent'], border_width=0)
        self.bedrag_inp.pack(side="left", padx=(0, 12))

        ctk.CTkLabel(inp, text="Omschrijving", text_color=COLORS['text_dim']).pack(side="left", padx=(0, 5))
        self.omschr_inp = ctk.CTkEntry(inp, width=120, fg_color=COLORS['accent'], border_width=0)
        self.omschr_inp.pack(side="left", padx=(0, 12))

        ctk.CTkButton(inp, text="Toevoegen", command=self.add_uitgave, fg_color=COLORS['orange'], hover_color="#ea580c", width=90, corner_radius=6, text_color="black").pack(side="left", padx=(0, 6))
        ctk.CTkButton(inp, text="Verwijder", command=self.del_uitgave, fg_color=COLORS['red'], hover_color="#dc2626", width=70, corner_radius=6).pack(side="left")

        tree_wrap = ctk.CTkFrame(self.tab2, fg_color=COLORS['accent'], corner_radius=10)
        tree_wrap.pack(fill="both", expand=True)

        self.tree2 = ttk.Treeview(tree_wrap, columns=('datum', 'bedrag', 'uren', 'omschr'), show='headings', style='T.Treeview', height=8)
        self.tree2.heading('datum', text='Datum')
        self.tree2.heading('bedrag', text='Bedrag')
        self.tree2.heading('uren', text='= Uren')
        self.tree2.heading('omschr', text='Omschrijving')
        self.tree2.column('datum', width=90, anchor='center')
        self.tree2.column('bedrag', width=70, anchor='center')
        self.tree2.column('uren', width=60, anchor='center')
        self.tree2.column('omschr', width=150)
        self.tree2.pack(fill="both", expand=True, padx=8, pady=8)

    def make_settings_tab(self):
        frame = ctk.CTkFrame(self.tab3, fg_color="transparent")
        frame.pack(pady=20)

        def row(label, default):
            r = ctk.CTkFrame(frame, fg_color="transparent")
            r.pack(fill="x", pady=6)
            ctk.CTkLabel(r, text=label, width=160, anchor="e").pack(side="left", padx=(0, 12))
            e = ctk.CTkEntry(r, width=100, fg_color=COLORS['accent'], border_width=0)
            e.pack(side="left")
            e.insert(0, str(default))
            return e

        self.s_doel = row("Doel uren:", self.data['maand_doel_uren'])
        self.s_uurloon = row("Uurloon €:", self.data['uurloon'])
        self.s_bruto = row("Bruto €:", self.data.get('bruto_totaal', 3800))
        self.s_netto = row("Netto €:", self.data.get('netto_totaal', 2217.87))

        ctk.CTkButton(frame, text="Opslaan", command=self.save_settings, fg_color=COLORS['purple'], hover_color="#9333ea", width=120, corner_radius=8).pack(pady=20)

    def get_dag(self, d):
        try:
            return ['Ma', 'Di', 'Wo', 'Do', 'Vr', 'Za', 'Zo'][datetime.strptime(d, "%d-%m-%Y").weekday()]
        except:
            return ""

    def refresh(self):
        for i in self.tree1.get_children():
            self.tree1.delete(i)
        for d in sorted(self.data['gewerkte_dagen'], key=lambda x: datetime.strptime(x['datum'], "%d-%m-%Y")):
            self.tree1.insert('', tk.END, values=(d['datum'], self.get_dag(d['datum']), d['uren'], d.get('notitie', '')))

        for i in self.tree2.get_children():
            self.tree2.delete(i)
        netto_per_uur = self.data.get('netto_totaal', 2217.87) / self.data['maand_doel_uren']
        for u in self.data['uitgaven_broertje']:
            self.tree2.insert('', tk.END, values=(u['datum'], f"€{u['bedrag']:.0f}", f"{u['bedrag']/netto_per_uur:.1f}", u.get('omschrijving', '')))

    def add_uren(self):
        try:
            self.data['gewerkte_dagen'].append({'datum': self.date1.get(), 'uren': float(self.uren_inp.get()), 'notitie': self.notitie_inp.get()})
            sla_data_op(self.data)
            self.uren_inp.delete(0, tk.END)
            self.notitie_inp.delete(0, tk.END)
            self.update_alles()
        except:
            messagebox.showerror("Fout", "Vul geldige uren in")

    def del_uren(self):
        sel = self.tree1.selection()
        if not sel:
            return
        v = self.tree1.item(sel[0])['values']
        self.data['gewerkte_dagen'] = [d for d in self.data['gewerkte_dagen'] if not (d['datum'] == v[0] and d['uren'] == float(v[2]))]
        sla_data_op(self.data)
        self.update_alles()

    def add_uitgave(self):
        try:
            self.data['uitgaven_broertje'].append({'datum': self.date2.get(), 'bedrag': float(self.bedrag_inp.get()), 'omschrijving': self.omschr_inp.get()})
            sla_data_op(self.data)
            self.bedrag_inp.delete(0, tk.END)
            self.omschr_inp.delete(0, tk.END)
            self.update_alles()
        except:
            messagebox.showerror("Fout", "Vul geldig bedrag in")

    def del_uitgave(self):
        sel = self.tree2.selection()
        if not sel:
            return
        v = self.tree2.item(sel[0])['values']
        bedrag = float(str(v[1]).replace('€', ''))
        for i, u in enumerate(self.data['uitgaven_broertje']):
            if u['datum'] == v[0] and abs(u['bedrag'] - bedrag) < 0.01:
                self.data['uitgaven_broertje'].pop(i)
                break
        sla_data_op(self.data)
        self.update_alles()

    def save_settings(self):
        try:
            self.data['maand_doel_uren'] = float(self.s_doel.get())
            self.data['uurloon'] = float(self.s_uurloon.get())
            self.data['bruto_totaal'] = float(self.s_bruto.get())
            self.data['netto_totaal'] = float(self.s_netto.get())
            sla_data_op(self.data)
            self.update_alles()
            messagebox.showinfo("OK", "Opgeslagen!")
        except:
            messagebox.showerror("Fout", "Ongeldige invoer")

    def update_alles(self):
        doel = self.data['maand_doel_uren']
        uurloon = self.data['uurloon']
        bruto = self.data.get('bruto_totaal', 3800)
        netto = self.data.get('netto_totaal', 2217.87)

        # Uren berekening
        gewerkt = sum(d['uren'] for d in self.data['gewerkte_dagen'])
        uitgaven_geld = sum(u['bedrag'] for u in self.data['uitgaven_broertje'])
        netto_per_uur = netto / doel
        uitgaven_uren = uitgaven_geld / netto_per_uur

        # Uitgaven tellen als gewerkte uren! Dus gaat ERAF van nog te werken
        totaal_gedaan = gewerkt + uitgaven_uren
        nog_te_werken = max(0, doel - totaal_gedaan)

        # Geld berekening
        # Nu verdiend = hoeveel je al hebt verdiend (gebaseerd op totaal gedaan)
        nu_verdiend = totaal_gedaan * netto_per_uur

        # Terug aan vader = alleen het geld dat je hebt besteed aan broertje
        terug_vader = uitgaven_geld

        # Jij houdt over = nu verdiend - terug aan vader
        jij_over = nu_verdiend - terug_vader

        # Update cards
        self.card1.lbl.configure(text=f"{gewerkt:.1f}")
        self.card2.lbl.configure(text=f"{nog_te_werken:.1f}")
        self.card3.lbl.configure(text=f"€{terug_vader:.0f}")
        self.card4.lbl.configure(text=f"€{jij_over:.0f}")

        # Kleur aanpassen als negatief
        if jij_over < 0:
            self.card4.lbl.configure(text_color=COLORS['red'])
        else:
            self.card4.lbl.configure(text_color=COLORS['purple'])

        # Update uren rows
        self.row_doel.configure(text=f"{doel} uur")
        self.row_gewerkt.configure(text=f"{gewerkt:.1f} uur")
        self.row_uitgaven_uren.configure(text=f"+{uitgaven_uren:.1f} uur")
        self.row_totaal_gedaan.configure(text=f"{totaal_gedaan:.1f} uur")
        self.row_nog.configure(text=f"{nog_te_werken:.1f} uur")
        self.row_uitgaven_geld.configure(text=f"€{uitgaven_geld:.0f}")

        # Update geld rows
        self.row_bruto.configure(text=f"€{bruto:,.0f}".replace(',', '.'))
        self.row_netto.configure(text=f"€{netto:,.2f}".replace(',', '.'))
        self.row_nu_verdiend.configure(text=f"€{nu_verdiend:,.0f}".replace(',', '.'))
        self.row_terug.configure(text=f"€{terug_vader:.0f}")
        self.row_over.configure(text=f"€{jij_over:.0f}")

        # Kleur voor jij houdt over
        if jij_over < 0:
            self.row_over.configure(text_color=COLORS['red'])
        else:
            self.row_over.configure(text_color=COLORS['purple'])

        self.refresh()

def main():
    app = UrenTrackerApp()
    app.mainloop()

if __name__ == "__main__":
    main()
