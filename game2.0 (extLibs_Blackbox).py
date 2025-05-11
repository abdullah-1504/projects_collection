from tkinter import ttk, messagebox, scrolledtext
import tkinter as tk
import random
from functools import partial

class FinancialTheftSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Theft Simulator: Shadow Heist")
        self.root.geometry("1200x750")
        self.root.resizable(False, False)
        self.root.configure(bg='#ecf0f1')

        # Full-screen state
        self.fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)  # Bind F11 to toggle full-screen

        # Initialize player count variable
        self.player_count = tk.IntVar(value=3)  # Default value is 3

        # Set the number of rounds for the game
        self.max_rounds = 5  # <-- Add this line

        # Initialize game components
        self.create_game_components()
        self.setup_ui()

        # Center the window after UI setup
        self.center_window(self.root, 1200, 750)

    def toggle_fullscreen(self, event=None):
        """
        Toggles the full-screen mode on or off.
        """
        self.fullscreen = not self.fullscreen
        self.root.attributes("-fullscreen", self.fullscreen)

    def center_window(self, window, width, height):
        """
        Centers the given window on the screen with the specified width and height.
        """
        if not self.fullscreen:  # Only center the window if not in full-screen mode
            window.update_idletasks()  # Ensure all geometry calculations are up-to-date
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            window.geometry(f'{width}x{height}+{x}+{y}')

    def create_game_components(self):
        self.car_cards = [
            {"name": "Basic Car", "cost": 10000, "risk": "Low",
             "narrative": ("The sedan is plain, almost forgettable. No attention, no suspicion...\n\n"
                           "You slip into the driver's seat, taking a deep breath, and drive off into the night."),
             "tagline": "A FISH IN A SEA OF PREDATORS"},
            {"name": "Luxury Car", "cost": 30000, "risk": "Medium",
             "narrative": ("People will notice the glint of your vehicle in the moonlight...\n\n"
                           "Can you afford to stand out? Or will your fame be your downfall?"),
             "tagline": "STYLE IN THE FACE OF DANGER"},
            {"name": "Sports Car", "cost": 50000, "risk": "High",
             "narrative": ("The roar of the engine is almost intoxicating...\n\n"
                           "The speed is your ally—but in this game, even the smallest misstep can turn it into your worst enemy."),
             "tagline": "POWER, SPEED, AND CHAOS"}
        ]
        self.crew_cards = [
            {"name": "Small Crew (2 people)", "cost": 20000, "risk": "Low",
             "narrative": ("Trust is the bedrock of your operation...\n\n"
                           "If something goes wrong, it's just the two of you against the world."),
             "tagline": "BLOOD BROTHERS IN CRIME"},
            {"name": "Medium Crew (4 people)", "cost": 50000, "risk": "Medium",
             "narrative": ("Four players, each with their own specialty...\n\n"
                           "There's strength in numbers, but there's also more room for things to go wrong."),
             "tagline": "FOUR AGAINST THE SYSTEM"},
            {"name": "Large Crew (6 people)", "cost": 80000, "risk": "High",
             "narrative": ("Six people in on the job...\n\n"
                           "You have to trust them all—but with this much risk, can you afford to?"),
             "tagline": "EVERYONE HAS A ROLE TO PLAY"}
        ]
        self.tech_cards = [
            {"name": "Basic Tools", "cost": 10000, "risk": "Low",
             "narrative": ("Simple tools, basic functionality...\n\n"
                           "The tools may be basic, but you're anything but."),
             "tagline": "OLD SCHOOL, HANDS-ON GRIT"},
            {"name": "Advanced Tools", "cost": 25000, "risk": "Medium",
             "narrative": ("High-tech gadgets, designed for precision...\n\n"
                           "One glitch, one wrong move, and the whole operation could collapse."),
             "tagline": "MODERN TECH FOR A PERFECT JOB"},
            {"name": "Cutting-Edge Tools", "cost": 50000, "risk": "High",
             "narrative": ("Nanobots for hacking, cloaking devices...\n\n"
                           "The high-tech world is full of risks, but with the right equipment, you're practically untouchable."),
             "tagline": "THE FUTURE IS NOW. BE CAREFUL"}
        ]
        self.financing_options = [
            {"name": "Equity Financing", "capital": 50000, "cost": "20% equity stake", "risk": "Medium",
             "narrative": ("You've sold part of your soul...\n\n"
                           "If you succeed, it's all worth it. But remember, they'll be watching."),
             "tagline": "THE PRICE OF AMBITION"},
            {"name": "Debt Financing", "capital": 30000, "cost": "Payback $34,500", "risk": "Medium",
             "narrative": ("The clock is ticking...\n\n"
                           "The pressure's on. This is the risk you take when you owe someone."),
             "tagline": "A LOAN FOR A LEGACY"},
            {"name": "Retained Earnings", "capital": 0, "cost": "No external cost", "risk": "Low",
             "narrative": ("No external help...\n\n"
                           "If you lose, you'll have no one to blame but yourself."),
             "tagline": "ALL IN, NO EXCUSES"}
        ]
        self.market_events = [
            {"name": "Police Interception", "effect": "Lose 5% capital, delay 1 turn",
             "narrative": ("The sirens blare in the distance...\n\n"
                           "The risk of failure just jumped exponentially."),
             "tagline": "IT'S A CLOSER CALL THAN YOU THINK"},
            {"name": "Tech Glitch", "effect": "Lose 7% capital, delay 1 turn",
             "narrative": ("Your digital lockpick short-circuits...\n\n"
                           "The tension is thick, and the clock is ticking faster now."),
             "tagline": "SYSTEM FAILURE. FIX IT FAST"},
            {"name": "Lucky Escape", "effect": "Lose 8% capital, gain extra turn",
             "narrative": ("A delivery truck cuts across the road...\n\n"
                           "You're not out of the woods yet, but this break might just be what you needed."),
             "tagline": "A NARROW ESCAPE"},
            {"name": "Clever Distraction", "effect": "Lose 12% capital, gain intel",
             "narrative": ("Smoke fills the area...\n\n"
                           "It's a risk, but it's working. The job's still on track."),
             "tagline": "SMOKE AND MIRRORS. IT WORKS"},
            {"name": "Unexpected Opportunity", "effect": "Lose 15% capital, delay, 10% bonus",
             "narrative": ("The rival company's breach gives you the perfect opening...\n\n"
                           "The heist just got a whole lot easier, but you know better than to trust luck for too long."),
             "tagline": "WHEN LUCK SMILES, TAKE IT"},
            {"name": "Police Undercover", "effect": "Lose 20% capital, delay 1 turn",
             "narrative": ("One of your crew members is an undercover cop...\n\n"
                           "The walls close in as you scramble to escape."),
             "tagline": "BETRAYAL BITES DEEP"}
        ]
        self.strategy_rewards = {
            "Loud": [200000, 210000, 220000, 230000, 240000],
            "Stealth": [80000, 90000, 100000, 110000, 120000]
        }

    def setup_ui(self):
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Configure grid to center the setup_frame
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Remove padx=200, pady=100 for true centering
        self.setup_frame = ttk.LabelFrame(self.main_frame, text="🕵️ Crew Assembly", padding=20)
        self.setup_frame.grid(row=0, column=0, sticky="")  # No sticky, no padding

        # Center the widgets inside setup_frame (optional, for better look)
        for i in range(2):
            self.setup_frame.grid_columnconfigure(i, weight=1)

        ttk.Label(self.setup_frame, text="Number of Operatives (3-4):", font=('Arial', 10)).grid(
            row=0, column=0, pady=5, sticky="e")
        ttk.Spinbox(self.setup_frame, from_=3, to_=4, textvariable=self.player_count, width=5).grid(
            row=0, column=1, pady=5, sticky="w")

        self.player_name_entries = []
        self.player_name_labels = []
        for i in range(4):
            label = ttk.Label(self.setup_frame, text=f"Operative {i+1} Alias:")
            label.grid(row=i+1, column=0, pady=2, sticky="e")
            entry = ttk.Entry(self.setup_frame)
            entry.grid(row=i+1, column=1, pady=2, sticky="w")
            self.player_name_entries.append(entry)
            self.player_name_labels.append(label)
            if i >= 3:  # Only hide the 4th player entry by default
                entry.grid_remove()
                label.grid_remove()

        self.player_count.trace_add("write", self.update_player_ui)

        ttk.Button(self.setup_frame, text="🚀 Initiate Heist", command=self.start_game, style='Accent.TButton').grid(
            row=5, column=0, columnspan=2, pady=10, sticky="ew")

        self.game_area = ttk.Frame(self.main_frame)
        self.game_area.grid_columnconfigure(0, weight=1)
        self.game_area.grid_rowconfigure(0, weight=1)
        self.game_area.grid_rowconfigure(1, weight=1)

        self.dashboard_frame = ttk.LabelFrame(self.game_area, text="📊 Operation Dashboard", padding=10)
        self.dashboard_frame.grid(row=0, column=0, sticky="nsew")
        self.controls_frame = ttk.LabelFrame(self.game_area, text="🎮 Mission Controls", padding=10)
        self.controls_frame.grid(row=1, column=0, sticky="nsew")

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Accent.TButton', foreground='white', background='#2c3e50', font=('Arial', 10, 'bold'))
        style.map('Accent.TButton', background=[('active', '#34495e')])
        style.configure('TLabelframe', background='#bdc3c7')
        style.configure('TLabelframe.Label', foreground='#2c3e50', font=('Arial', 12, 'bold'))
        style.configure('TLabel', background='#ecf0f1', foreground='#2c3e50')
        style.configure('TButton', background='#2980b9', foreground='white')
        style.map('TButton',
              foreground=[('pressed', 'white'), ('active', 'white')], 
              background=[('pressed', '#1c5980'), ('active', '#3498db')])

    def update_player_ui(self, *args):
        count = self.player_count.get()
        for i in range(4):
            if i < count:
                self.player_name_entries[i].grid()
                self.player_name_labels[i].grid()
            else:
                self.player_name_entries[i].grid_remove()
                self.player_name_labels[i].grid_remove()

    def show_narrative_popup(self, title, narrative, tagline):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.configure(bg='#ecf0f1')
        popup.grab_set()

        # Calculate and center the window
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width // 2) - (600 // 2)
        y = (screen_height // 2) - (400 // 2)
        popup.geometry(f"600x400+{x}+{y}")

        main_frame = ttk.Frame(popup, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text=tagline, font=('Arial', 12, 'bold'), wraplength=550, foreground='#34495e').pack(pady=5)
        ttk.Separator(main_frame, orient='horizontal').pack(fill=tk.X, pady=5)

        # ScrolledText widget to display narrative
        text_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=12, font=('Arial', 10))
        text_area.insert(tk.INSERT, narrative)
        text_area.configure(state='disabled', background='#f8f9fa', foreground='#2c3e50')
        text_area.pack(pady=10)

        ttk.Button(main_frame, text="Continue", command=popup.destroy, style='Accent.TButton').pack()

    def start_game(self):
        player_names = []
        count = self.player_count.get()
        for i in range(count):
            name = self.player_name_entries[i].get().strip()
            if not name:
                messagebox.showerror("Error", f"Enter alias for Operative {i+1}")
                return
            player_names.append(name)
        self.players = []
        for name in player_names:
            self.players.append({
                "name": name, "capital": 100000, "strategy": None,
                "car": None, "crew": None, "tech": None, "financing": None,
                "investments": [], "market_events": [], "delayed": False,
                "bonus_next_round": 0, "intel_bonus": False, "extra_turn": False,
                "total_investment": 0, "npv": 0, "irr": 0, "payback_period": 0, "roi": 0
            })
        self.setup_frame.grid_remove()
        self.game_area.grid(row=0, column=0, sticky="nsew")
        self.game_started = True
        self.current_player_index = 0
        self.current_round = 1
        self.update_dashboard()
        self.show_strategy_selection()

    def update_dashboard(self):
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
        current_player = self.players[self.current_player_index]
        ttk.Label(self.dashboard_frame, text=f"🔦 OPERATIVE: {current_player['name']}", 
                  font=('Arial', 12, 'bold'), foreground='#2c3e50').grid(row=0, column=0, sticky="w")
        ttk.Label(self.dashboard_frame, text=f"🕒 ROUND: {self.current_round}/{self.max_rounds}", 
                  font=('Arial', 12)).grid(row=0, column=1, sticky="w")
        ttk.Label(self.dashboard_frame, text=f"💰 CAPITAL: ${current_player['capital']:,}", 
                  font=('Arial', 12)).grid(row=1, column=0, sticky="w")
        strategy = current_player.get('strategy')
        strategy_text = f"🎯 STRATEGY: {strategy}" if strategy else "🎯 STRATEGY: PENDING"
        ttk.Label(self.dashboard_frame, text=strategy_text, font=('Arial', 12)).grid(row=1, column=1, sticky="w")
        resources = []
        if current_player.get('car'): resources.append(f"🚗 {current_player['car']['name']}")
        if current_player.get('crew'): resources.append(f"👥 {current_player['crew']['name']}")
        if current_player.get('tech'): resources.append(f"🔧 {current_player['tech']['name']}")
        resources_text = " | ".join(resources) if resources else "📦 RESOURCES: PENDING"
        ttk.Label(self.dashboard_frame, text=resources_text, font=('Arial', 12)).grid(row=2, column=0, columnspan=2, sticky="w")
        financing = current_player.get('financing')
        financing_text = f"💳 FINANCING: {financing['name']}" if financing else "💳 FINANCING: PENDING"
        ttk.Label(self.dashboard_frame, text=financing_text, font=('Arial', 12)).grid(row=3, column=0, columnspan=2, sticky="w")
        metrics_frame = ttk.Frame(self.dashboard_frame)
        metrics_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
        ttk.Label(metrics_frame, text="📈 NPV:", font=('Arial', 11)).grid(row=0, column=0, padx=5)
        ttk.Label(metrics_frame, text=f"${current_player['npv']:,.2f}", font=('Arial', 11, 'bold')).grid(row=0, column=1, padx=5)
        ttk.Label(metrics_frame, text="📊 IRR:", font=('Arial', 11)).grid(row=0, column=2, padx=5)
        ttk.Label(metrics_frame, text=f"{current_player['irr']:.2f}%", font=('Arial', 11, 'bold')).grid(row=0, column=3, padx=5)
        ttk.Label(metrics_frame, text="⏳ Payback:", font=('Arial', 11)).grid(row=0, column=4, padx=5)
        ttk.Label(metrics_frame, text=f"{current_player['payback_period']} rounds", font=('Arial', 11, 'bold')).grid(row=0, column=5, padx=5)
        ttk.Label(metrics_frame, text="📉 ROI:", font=('Arial', 11)).grid(row=0, column=6, padx=5)
        ttk.Label(metrics_frame, text=f"{current_player['roi']:.2f}%", font=('Arial', 11, 'bold')).grid(row=0, column=7, padx=5)
        if current_player.get('market_events'):
            events = current_player['market_events']
            if events:
                events_frame = ttk.LabelFrame(self.dashboard_frame, text="🚨 ACTIVE EVENTS", padding=5)
                events_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)
                for i, event in enumerate(events):
                    ttk.Label(events_frame, text=f"• {event['name']}: {event['effect']}",
                              font=('Arial', 10)).grid(row=i, column=0, sticky="w")

    def show_strategy_selection(self):
        for widget in self.controls_frame.winfo_children():
            widget.destroy()
        current_player = self.players[self.current_player_index]
        if current_player.get('delayed'):
            current_player['delayed'] = False
            messagebox.showinfo("Delayed", f"{current_player['name']} was delayed last round!")
            self.next_player()
            return
        ttk.Label(self.controls_frame, text="🔫 SELECT HEIST STRATEGY:",
                  font=('Arial', 12, 'bold'), foreground='#34495e').pack(pady=10)
        btn_frame = ttk.Frame(self.controls_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="💥 LOUD", width=25,
                  command=lambda: [self.show_narrative_popup("LOUD STRATEGY",
                   ("You've had enough of silence. The plan is simple: make a statement.\n\n"
                    "The louder you roar, the more attention you draw. You'll either walk away with everything—"
                    "or you'll go down in flames."), "MAKE NOISE. MAKE A LEGEND."),
                   self.select_strategy("Loud")], style='Accent.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🕶️ STEALTH", width=25,
                  command=lambda: [self.show_narrative_popup("STEALTH STRATEGY",
                   ("The heist has to be quiet, almost invisible...\n\n"
                    "The plan is to get in, get out, and leave the system none the wiser. "
                    "But remember, one mistake and you could find yourself vanished without a trace."),
                    "IN THE DARKNESS, YOU ARE THE KING."),
                   self.select_strategy("Stealth")], style='Accent.TButton').pack(side=tk.LEFT, padx=5)

    def select_strategy(self, strategy):
        current_player = self.players[self.current_player_index]
        current_player['strategy'] = strategy
        self.update_dashboard()
        self.show_resource_selection()

    def show_resource_selection(self):
        for widget in self.controls_frame.winfo_children():
            widget.destroy()
        current_player = self.players[self.current_player_index]
        ttk.Label(self.controls_frame, text="🔧 SELECT RESOURCES:",
                  font=('Arial', 12, 'bold'), foreground='#34495e').pack(pady=10)
        # Fix: Added fixed height to canvas for better scrolling of tech selection
        canvas_height = 400
        canvas = tk.Canvas(self.controls_frame, bg='#ecf0f1', height=canvas_height, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.controls_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.create_resource_section(scrollable_frame, "🚗 VEHICLE SELECTION", self.car_cards, 'car', current_player)
        self.create_resource_section(scrollable_frame, "👥 CREW SELECTION", self.crew_cards, 'crew', current_player)
        self.create_resource_section(scrollable_frame, "🔧 TECH SELECTION", self.tech_cards, 'tech', current_player)
        if current_player.get('car') and current_player.get('crew') and current_player.get('tech'):
            ttk.Button(self.controls_frame, text="🚀 CONTINUE TO FINANCING",
                       command=self.show_financing_selection, style='Accent.TButton').pack(pady=10)

    def create_resource_section(self, parent, title, items, resource_type, player):
        frame = ttk.LabelFrame(parent, text=title, padding=10)
        frame.pack(fill=tk.X, padx=5, pady=5)
        for item in items:
            btn_frame = ttk.Frame(frame)
            btn_frame.pack(fill=tk.X, pady=2)
            btn = ttk.Button(btn_frame, text=f"{item['name']} (${item['cost']:,})",
                             command=partial(self.select_resource, resource_type, item),
                             width=30)
            btn.pack(side=tk.LEFT)
            ttk.Label(btn_frame, text=f"Risk: {item['risk']}", width=15).pack(side=tk.LEFT)
            if item['cost'] > player.get('capital', 0):
                btn.state(['disabled'])
            ttk.Button(btn_frame, text="📖", width=3,
                      command=lambda i=item: self.show_narrative_popup(
                          i['name'], i['narrative'], i['tagline'])
                      ).pack(side=tk.RIGHT)

    def select_resource(self, resource_type, resource):
        current_player = self.players[self.current_player_index]
        previous = current_player.get(resource_type)
        if previous:
            current_player['capital'] += previous['cost']
        current_player[resource_type] = resource
        current_player['capital'] -= resource['cost']
        self.update_dashboard()
        self.show_resource_selection()

    def show_financing_selection(self):
        if self.current_round > 1:
            self.draw_market_event()
            return
        for widget in self.controls_frame.winfo_children():
            widget.destroy()
        current_player = self.players[self.current_player_index]
        ttk.Label(self.controls_frame, text="💸 FINANCING OPTIONS:",
                  font=('Arial', 12, 'bold'), foreground='#34495e').pack(pady=10)
        for financing in self.financing_options:
            frame = ttk.Frame(self.controls_frame, padding=10, relief="ridge")
            frame.pack(fill=tk.X, padx=5, pady=5)
            ttk.Label(frame, text=financing['name'], font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky="w")
            ttk.Button(frame, text="📖", command=lambda f=financing: self.show_narrative_popup(
                f['name'], f['narrative'], f['tagline'])).grid(row=0, column=1)
            ttk.Label(frame, text=f"Capital: ${financing['capital']:,}").grid(row=1, column=0, sticky="w")
            ttk.Label(frame, text=f"Risk: {financing['risk']}").grid(row=2, column=0, sticky="w")
            ttk.Button(frame, text="Select", style='Accent.TButton',
                      command=partial(self.select_financing, financing)).grid(row=0, column=2, rowspan=3)

    def select_financing(self, financing):
        current_player = self.players[self.current_player_index]
        prev_financing = current_player.get('financing')
        if prev_financing:
            current_player['capital'] -= prev_financing['capital']
        current_player['financing'] = financing
        current_player['capital'] += financing['capital']
        self.update_dashboard()
        self.draw_market_event()

    def draw_market_event(self):
        for widget in self.controls_frame.winfo_children():
            widget.destroy()
        current_player = self.players[self.current_player_index]
        event = random.choice(self.market_events)
        severity = random.randint(1, 12)
        effect_map = {
            "Police Interception": (0.05, "delayed"),
            "Tech Glitch": (0.07, "delayed"),
            "Lucky Escape": (0.08, "extra_turn"),
            "Clever Distraction": (0.12, "intel_bonus"),
            "Unexpected Opportunity": (0.15, "bonus_next_round"),
            "Police Undercover": (0.20, "delayed")
        }
        loss_percent, effect_type = effect_map[event['name']]
        capital_loss = current_player['capital'] * loss_percent
        current_player['capital'] -= capital_loss
        if effect_type == "bonus_next_round":
            current_player[effect_type] = 0.10
        else:
            current_player[effect_type] = True
        current_player['market_events'].append({
            "name": event['name'],
            "effect": event['effect'],
            "severity": severity
        })
        self.calculate_financials(current_player)
        self.show_narrative_popup("🚨 MARKET EVENT",
                                  f"{event['narrative']}\n\nSeverity Roll: {severity}/12\nCapital Lost: ${capital_loss:,.2f}",
                                  event['tagline'])
        # Ensure the game progresses after the market event
        ttk.Button(self.controls_frame, text="⏭️ CONTINUE",
                   command=self.next_player, style='Accent.TButton').pack(pady=10)

    def calculate_financials(self, player):
        total_investment = sum([
            player['car']['cost'] if player.get('car') else 0,
            player['crew']['cost'] if player.get('crew') else 0,
            player['tech']['cost'] if player.get('tech') else 0
        ])
        player['total_investment'] = total_investment
        strategy = player.get('strategy')
        if not strategy:
            player['npv'] = 0
            player['irr'] = 0
            player['payback_period'] = 0
            player['roi'] = 0
            return
        reward = random.choice(self.strategy_rewards.get(strategy, [0]))
        if player.get('intel_bonus'):
            reward *= 1.15
        if player.get('bonus_next_round'):
            reward *= 1.10
        discount_rate = 0.10
        player['npv'] = -total_investment + (reward / (1 + discount_rate))
        player['irr'] = ((reward / total_investment) - 1) * 100 if total_investment else 0
        player['payback_period'] = round(total_investment / reward * self.max_rounds, 1) if reward else 0
        player['roi'] = ((reward - total_investment) / total_investment) * 100 if total_investment else 0

    def next_player(self):
        current_player = self.players[self.current_player_index]
        current_player['bonus_next_round'] = 0
        current_player['intel_bonus'] = False
        if current_player.get('extra_turn'):
            current_player['extra_turn'] = False
            messagebox.showinfo("Extra Turn", f"{current_player['name']} gets an extra turn!")
            self.update_dashboard()
            self.show_strategy_selection()
            return
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.current_player_index = 0
            self.current_round += 1
            if self.current_round > self.max_rounds:
                self.end_game()
                return
        self.update_dashboard()
        self.show_strategy_selection()

    def end_game(self):
        for player in self.players:
            reward = random.choice(self.strategy_rewards.get(player.get('strategy'), [0]))
            if player.get('financing') and player['financing']['name'] == "Debt Financing":
                player['capital'] -= 34500
            player['capital'] += reward
            total_investment = player.get('total_investment', 0)
            player['roi'] = ((reward - total_investment) / total_investment) * 100 if total_investment else 0
            # Ensure NPV is up to date
            discount_rate = 0.10
            player['npv'] = -total_investment + (reward / (1 + discount_rate))

        # Determine winners
        strategic_winner = max(self.players, key=lambda p: p.get('npv', 0))
        efficiency_winner = max(self.players, key=lambda p: p.get('roi', 0))

        result_window = tk.Toplevel(self.root)
        result_window.title("🏁 Heist Conclusion")
        result_window.geometry("800x600")
        result_window.configure(bg='#ecf0f1')
        self.center_window(result_window, 800, 600)
        main_frame = ttk.Frame(result_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        for player in self.players:
            roi = player.get('roi', 0)
            npv = player.get('npv', 0)
            if roi > 50:
                conclusion = "🌟 THE LEGEND BEGINS: You're now a myth in the criminal underworld!"
            elif 20 <= roi <= 50:
                conclusion = "👻 YOU'RE THE GHOST IN THE SYSTEM: The perfect invisible heist!"
            else:
                conclusion = "💥 BURNED MARK: Better luck next time in the shadows..."

            # Highlight winners
            winner_tags = []
            if player is strategic_winner:
                winner_tags.append("🏆 Strategic Winner (Highest NPV)")
            if player is efficiency_winner:
                winner_tags.append("⚡ Efficiency Winner (Highest ROI)")
            winner_text = " | ".join(winner_tags)
            if winner_text:
                conclusion = f"{conclusion}\n{winner_text}"

            player_frame = ttk.LabelFrame(main_frame, text=f"🔦 {player['name']}", padding=10)
            player_frame.pack(fill=tk.X, pady=5)
            ttk.Label(player_frame, text=conclusion, font=('Arial', 11, 'bold'), foreground='#2c3e50').grid(row=0, column=0, sticky="w")
            ttk.Label(player_frame, text=f"Final Capital: ${player['capital']:,.2f}\nNPV: ${npv:,.2f}\nROI: {roi:.2f}%",
                      font=('Arial', 10), foreground='#2c3e50').grid(row=1, column=0, sticky="w")

        ttk.Button(main_frame, text="🔚 Exit", command=self.root.destroy, style='Accent.TButton').pack(pady=10)

if __name__ == '__main__':
    root = tk.Tk()
    app = FinancialTheftSimulator(root)
    root.mainloop()
