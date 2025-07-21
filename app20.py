from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup

class MenuAppOpciones(App):
    def build(self):
        self.comanda = []
        self.opciones_seleccion = {}
        self.banchan_seleccionados = []
        self.mesa_seleccionada = None
        self.alergenos_seleccionados = []

        root = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Selector de mesa
        mesas = ['M1', 'M2', 'M3', 'M4', 'M5', 'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8']
        root.add_widget(Label(text="Selecciona Mesa:", size_hint=(1,None), height=30, font_size=14))

        self.spinner_mesa = Spinner(
            text='Elige mesa',
            values=mesas,
            size_hint=(None, None),
            size=(150, 30),
            font_size=14
        )
        self.spinner_mesa.bind(text=self.on_mesa_select)
        root.add_widget(self.spinner_mesa)

        self.lbl_mesa = Label(text="Mesa seleccionada: Ninguna", size_hint=(1,None), height=30, font_size=14)
        root.add_widget(self.lbl_mesa)

        # Selector de menú - Platos y Bebidas
        root.add_widget(Label(text="Selecciona Plato o Bebida:", size_hint=(1,None), height=30, font_size=14))

        opciones_platos = [
            'MANDU', 'GIMBAP', 'JEMULYEON', 'RAMYUN', 'TTEOKBOKKI', 'CREAM TTEOKBOKKI', 'ROSE TTEOKBOKKI',
            'DENGJANGKUK', 'KIMCHIJIGAE', 'DAKGANGYEONG KIMCHIMAYO', 'KIMCHICKEN', 'DAKGANGYEONG PICANTE',
            'DAKGANGYEONG SOJA Y AJO', 'DAKGANG YEONG XL', 'BULGOGUI DEOBAP', 'BIBIMBAP', 'DOLSOT BIBIMBAP',
            'ARROZ', 'KIMCHI', 'JUMEOK-BAP', 'BEKBAN', 'DOSIRAK', 'BANCHAN', 'BARBACOA'
        ]

        opciones_bebidas = [
            'Estrella 1906', 'Caña', 'Estrella Tercio', 'Cass', 'Alhambra 1925', 'Cerveza sin alcohol',
            'Agua', 'Agua con gas', 'Fanta Naranja', 'Fanta Limón', 'Cola Cero', 'Cola Original',
            'Nestea Limón', 'Nestea Mango Piña', 'Aquarius Limón', 'Aquarius Naranja', 'Sprite',
            'Agua Tónica', 'Korea Uva', 'Korea Coco Uva', 'Korea Melocotón', 'Korea Fresa',
            'Cocktail Soju',
            'Ron', 'Ginebra', 'Whisky', 'Vodka',
            'Vino Blanco - Bascarlon (Rueda)', 'Vino Blanco - Viña Albina (Semidulce)',
            'Vino Blanco - Viore (Verdejo)', 'Vino Blanco - Beronia (Verdejo)',
            'Vino Tinto - Un Roble (Ribera)', 'Vino Tinto - Puerta Vieja Crianza (Rioja)',
            'Vino Tinto - Azpilicueta Crianza (Rioja)', 'Vino Tinto - Beronia Reserva (Rioja)',
            'Botella Soju Melocotón', 'Botella Soju Uva', 'Botella Soju Manzana',
            'Botella Soju Original', 'Botella Soju Fresa',
            'Chupito Soju Melocotón', 'Chupito Soju Uva', 'Chupito Soju Manzana',
            'Chupito Soju Original', 'Chupito Soju Fresa',
            'Botella Makgeolli Melocotón', 'Botella Makgeolli Uva', 'Botella Makgeolli Plátano', 'Botella Makgeolli Original',
            'Chupito Makgeolli Melocotón', 'Chupito Makgeolli Uva', 'Chupito Makgeolli Plátano', 'Chupito Makgeolli Original'
        ]

        box_menus = BoxLayout(size_hint=(1,None), height=40, spacing=10)

        self.spinner_platos = Spinner(
            text='Elige plato',
            values=opciones_platos,
            size_hint=(None,None),
            size=(150,30),
            font_size=14
        )
        self.spinner_platos.bind(text=self.seleccionar_plato)

        self.spinner_bebidas = Spinner(
            text='Elige bebida',
            values=opciones_bebidas,
            size_hint=(None,None),
            size=(200,30),
            font_size=14
        )
        self.spinner_bebidas.bind(text=self.seleccionar_bebida)

        box_menus.add_widget(self.spinner_platos)
        box_menus.add_widget(self.spinner_bebidas)

        root.add_widget(box_menus)

        # Botón Alérgenos
        self.btn_alergenos = Button(text="Alérgenos", size_hint=(None,None), size=(100, 30), font_size=14)
        self.btn_alergenos.bind(on_press=self.mostrar_popup_alergenos)
        root.add_widget(self.btn_alergenos)

        # Opciones para platos (y bebidas que necesiten opciones)
        self.opciones_layout = BoxLayout(orientation='vertical', size_hint=(1, None), height=300)
        root.add_widget(self.opciones_layout)

        # Comanda
        root.add_widget(Label(text="Comanda:", size_hint=(1,None), height=30))
        self.comanda_label = Label(text="", size_hint=(1,None), height=150)
        root.add_widget(self.comanda_label)

        # Botón Enviar a Cocina
        self.btn_enviar = Button(text="Enviar a Cocina", size_hint=(None,None), size=(150, 40), font_size=14)
        self.btn_enviar.bind(on_press=self.enviar_a_cocina)
        root.add_widget(self.btn_enviar)

        return root

    def mostrar_popup_alergenos(self, instance):
        alergenos = [
            'Gluten', 'Crustáceos', 'Huevo', 'Pescado', 'Cacahuetes',
            'Soja', 'Lácteos', 'Frutos de cáscara', 'Apio', 'Mostaza',
            'Sésamo', 'Sulfitos', 'Moluscos', 'Altramuces', 'Mariscos'
        ]
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.checkbox_dict = {}
        grid = GridLayout(cols=2, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        for alergeno in alergenos:
            box = BoxLayout(size_hint_y=None, height=30)
            cb = CheckBox()
            lbl = Label(text=alergeno, size_hint_x=None, width=150, font_size=14)
            box.add_widget(cb)
            box.add_widget(lbl)
            grid.add_widget(box)
            self.checkbox_dict[alergeno] = cb

        scroll = ScrollView(size_hint=(1, None), height=250)
        scroll.add_widget(grid)
        content.add_widget(scroll)

        btn_ok = Button(text="Confirmar", size_hint=(1,None), height=40, font_size=14)
        btn_ok.bind(on_press=self.confirmar_alergenos)
        content.add_widget(btn_ok)

        self.popup_alergenos = Popup(title="Selecciona Alérgenos", content=content, size_hint=(0.7, 0.7))
        self.popup_alergenos.open()

    def confirmar_alergenos(self, instance):
        seleccionados = [alergeno for alergeno, cb in self.checkbox_dict.items() if cb.active]
        self.alergenos_seleccionados = seleccionados
        self.popup_alergenos.dismiss()

        if not self.mesa_seleccionada or self.mesa_seleccionada == 'Elige mesa':
            # No mesa seleccionada, mostrar aviso
            self.opciones_layout.clear_widgets()
            self.opciones_layout.add_widget(Label(text="Selecciona una mesa antes de añadir alérgenos.", font_size=14, color=(1,0,0,1)))
            return

        if not self.alergenos_seleccionados:
            self.comanda.append(f"Mesa {self.mesa_seleccionada}: Sin alérgenos especificados")
        else:
            alergenos_str = ", ".join(self.alergenos_seleccionados)
            self.comanda.append(f"Mesa {self.mesa_seleccionada}: Alérgenos - {alergenos_str}")

        self.actualizar_comanda()

    def on_mesa_select(self, spinner, text):
        self.mesa_seleccionada = text
        self.lbl_mesa.text = f"Mesa seleccionada: {text}"

    def seleccionar_plato(self, spinner, text):
        if text == 'Elige plato':
            return
        self.spinner_bebidas.text = 'Elige bebida'

        if not self.mesa_seleccionada or self.mesa_seleccionada == 'Elige mesa':
            self.opciones_layout.clear_widgets()
            self.opciones_layout.add_widget(Label(text="Por favor selecciona una mesa antes de elegir un plato.", font_size=14, color=(1,0,0,1)))
            self.spinner_platos.text = 'Elige plato'
            return

        self.opciones_layout.clear_widgets()
        self.banchan_seleccionados = []
        self.opciones_seleccion = {'plato': text}

        plato = text

        if plato == 'MANDU':
            self.crear_spinner("Tipo de MANDU:", ['vegetal', 'carne', 'mixto'], 'tipo')
            self.boton_añadir()

        elif plato == 'GIMBAP':
            self.crear_spinner("Tipo de GIMBAP:", ['vegetal', 'carne'], 'tipo')
            self.boton_añadir()

        elif plato == 'RAMYUN':
            self.crear_spinner("Tipo de RAMYUN:", ['mariscos', 'empanadillas carne', 'empanadillas vegetal'], 'tipo')
            self.boton_añadir()

        elif plato == 'TTEOKBOKKI':
            self.crear_spinner("Extra:", ['sin extra', 'queso', 'fideos'], 'extra')
            self.boton_añadir()

        elif plato == 'BULGOGUI DEOBAP':
            self.crear_spinner("Guarnición:", ['arroz', 'udon', 'fideos de batata'], 'guarnicion')
            self.boton_añadir()

        elif plato in ['BIBIMBAP', 'DOLSOT BIBIMBAP']:
            self.crear_spinner("Salsa:", ['gochujang', 'teriyaki', 'ssamjang', 'curry mango'], 'salsa')
            self.crear_spinner("Proteína:", ['carne', 'tofu'], 'proteina')
            self.boton_añadir()

        elif plato in ['BEKBAN', 'DOSIRAK']:
            self.opciones_layout.add_widget(Label(text="Selecciona proteína:", size_hint=(None,None), size=(150,30), font_size=14))
            box_prot = BoxLayout(size_hint_y=None, height=30, spacing=10)
            for prot in ['bulgogui', 'tofu']:
                btn = Button(text=prot, size_hint=(None,None), size=(100,30), font_size=14)
                btn.bind(on_press=self.seleccionar_proteina)
                box_prot.add_widget(btn)
            self.opciones_layout.add_widget(box_prot)

            self.opciones_layout.add_widget(Label(text="Selecciona 3 banchan (pueden repetirse):", size_hint=(None,None), size=(300,30), font_size=14))
            banchan_list = ['GUERANMARY', 'OI MUCHIM', 'SIGUEUMCHI MUCHIM', 'GAJI BOKKEUM', 'KIM', 'KIMCHI', 'HOBAKJEON']
            grid_banchan = GridLayout(cols=3, size_hint_y=None)
            grid_banchan.bind(minimum_height=grid_banchan.setter('height'))
            for b in banchan_list:
                btn = Button(text=b, size_hint=(None,None), size=(100,30), font_size=14)
                btn.bind(on_press=self.seleccionar_banchan)
                grid_banchan.add_widget(btn)
            scroll_banchan = ScrollView(size_hint=(1, None), height=100)
            scroll_banchan.add_widget(grid_banchan)
            self.opciones_layout.add_widget(scroll_banchan)

            self.lbl_seleccionados = Label(text="Proteína: Ninguna | Banchan: []", size_hint=(None,None), size=(300,30), font_size=14)
            self.opciones_layout.add_widget(self.lbl_seleccionados)

            btn_add = Button(text="Añadir a comanda", size_hint=(None,None), size=(150,30), font_size=14)
            btn_add.bind(on_press=self.añadir_bekban_dosirak)
            self.opciones_layout.add_widget(btn_add)

        else:
            self.comanda.append(f"Mesa {self.mesa_seleccionada}: {plato}")
            self.actualizar_comanda()
            self.opciones_layout.clear_widgets()
            self.spinner_platos.text = 'Elige plato'

    def seleccionar_bebida(self, spinner, text):
        if text == 'Elige bebida':
            return
        self.spinner_platos.text = 'Elige plato'

        if not self.mesa_seleccionada or self.mesa_seleccionada == 'Elige mesa':
            self.opciones_layout.clear_widgets()
            self.opciones_layout.add_widget(Label(text="Por favor selecciona una mesa antes de elegir una bebida.", font_size=14, color=(1,0,0,1)))
            self.spinner_bebidas.text = 'Elige bebida'
            return

        self.opciones_layout.clear_widgets()
        self.opciones_seleccion = {'bebida': text}

        # Si es cocktail soju, lanzar opciones de tipo, alcohol y sabor
        if text == 'Cocktail Soju':
            self.crear_spinner("Tipo de Cocktail:", ['Copa', 'Jarra'], 'tipo_cocktail')
            self.crear_spinner("Alcohol:", ['Con alcohol', 'Sin alcohol'], 'alcohol')
            self.crear_spinner("Sabor:", ['mango', 'lima', 'uva', 'arándanos'], 'sabor')
            self.boton_añadir()
        else:
            self.comanda.append(f"Mesa {self.mesa_seleccionada}: {text}")
            self.actualizar_comanda()
            self.opciones_layout.clear_widgets()
            self.spinner_bebidas.text = 'Elige bebida'

    def crear_spinner(self, texto, opciones, key):
        self.opciones_layout.add_widget(Label(text=texto, size_hint=(None,None), size=(200,30), font_size=14))
        spinner = Spinner(text=opciones[0], values=opciones, size_hint=(None,None), size=(150,30), font_size=14)
        spinner.bind(text=lambda spinner, val: self.opciones_seleccion.update({key: val}))
        self.opciones_seleccion[key] = opciones[0]
        self.opciones_layout.add_widget(spinner)

    def boton_añadir(self):
        btn = Button(text="Añadir a comanda", size_hint=(None,None), size=(150,30), font_size=14)
        btn.bind(on_press=self.añadir_a_comanda)
        self.opciones_layout.add_widget(btn)

    def añadir_a_comanda(self, instance):
        if not self.mesa_seleccionada or self.mesa_seleccionada == 'Elige mesa':
            self.opciones_layout.clear_widgets()
            self.opciones_layout.add_widget(Label(text="Selecciona una mesa antes de añadir a la comanda.", font_size=14, color=(1,0,0,1)))
            return

        detalles = []
        for k, v in self.opciones_seleccion.items():
            if k != 'plato' and k != 'bebida':
                detalles.append(f"{k}: {v}")
        if 'plato' in self.opciones_seleccion:
            texto = f"Mesa {self.mesa_seleccionada}: {self.opciones_seleccion['plato']}"
            if detalles:
                texto += " (" + ", ".join(detalles) + ")"
            self.comanda.append(texto)
        elif 'bebida' in self.opciones_seleccion:
            texto = f"Mesa {self.mesa_seleccionada}: {self.opciones_seleccion['bebida']}"
            if detalles:
                texto += " (" + ", ".join(detalles) + ")"
            self.comanda.append(texto)

        self.actualizar_comanda()
        self.opciones_layout.clear_widgets()
        self.spinner_platos.text = 'Elige plato'
        self.spinner_bebidas.text = 'Elige bebida'

    def seleccionar_proteina(self, instance):
        self.opciones_seleccion['proteina'] = instance.text
        self.actualizar_lbl_bekban_dosirak()

    def seleccionar_banchan(self, instance):
        if len(self.banchan_seleccionados) < 3:
            self.banchan_seleccionados.append(instance.text)
        else:
            # si ya hay 3, reemplazamos el primero para permitir "cambios"
            self.banchan_seleccionados.pop(0)
            self.banchan_seleccionados.append(instance.text)
        self.actualizar_lbl_bekban_dosirak()

    def actualizar_lbl_bekban_dosirak(self):
        prot = self.opciones_seleccion.get('proteina', 'Ninguna')
        banchan = self.banchan_seleccionados
        self.lbl_seleccionados.text = f"Proteína: {prot} | Banchan: {banchan}"

    def añadir_bekban_dosirak(self, instance):
        if not self.mesa_seleccionada or self.mesa_seleccionada == 'Elige mesa':
            self.opciones_layout.clear_widgets()
            self.opciones_layout.add_widget(Label(text="Selecciona una mesa antes de añadir a la comanda.", font_size=14, color=(1,0,0,1)))
            return

        if 'proteina' not in self.opciones_seleccion:
            self.opciones_layout.clear_widgets()
            self.opciones_layout.add_widget(Label(text="Selecciona una proteína.", font_size=14, color=(1,0,0,1)))
            return

        if len(self.banchan_seleccionados) != 3:
            self.opciones_layout.clear_widgets()
            self.opciones_layout.add_widget(Label(text="Selecciona exactamente 3 banchan.", font_size=14, color=(1,0,0,1)))
            return

        texto = f"Mesa {self.mesa_seleccionada}: {self.opciones_seleccion['plato']} con proteína {self.opciones_seleccion['proteina']} y banchan {', '.join(self.banchan_seleccionados)}"
        self.comanda.append(texto)
        self.actualizar_comanda()
        self.opciones_layout.clear_widgets()
        self.spinner_platos.text = 'Elige plato'
        self.banchan_seleccionados = []
        self.opciones_seleccion = {}

    def actualizar_comanda(self):
        self.comanda_label.text = "\n".join(self.comanda)

    def enviar_a_cocina(self, instance):
        if not self.comanda:
            self.mostrar_popup_mensaje("La comanda está vacía.")
            return

        texto_comanda = "\n".join(self.comanda)
        self.mostrar_popup_mensaje(f"Comanda enviada a cocina:\n\n{texto_comanda}")

    def mostrar_popup_mensaje(self, mensaje):
        contenido = BoxLayout(orientation='vertical', padding=10)
        contenido.add_widget(Label(text=mensaje, font_size=14))
        btn_cerrar = Button(text="Cerrar", size_hint=(1,None), height=40)
        popup = Popup(title="Información", content=contenido, size_hint=(0.7, 0.5))
        btn_cerrar.bind(on_press=popup.dismiss)
        contenido.add_widget(btn_cerrar)
        popup.open()


if __name__ == '__main__':
    MenuAppOpciones().run()
