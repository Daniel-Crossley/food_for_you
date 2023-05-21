import kivy
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'width', '1024')
Config.set('graphics', 'height', '727')
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'vsync', '1')
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
import requests
import sqlite3
import hashlib
from sqlite3 import Error
Window.clearcolor = (0.7, 0.7, 0.7, 1)
ActiveButtons = []
Username = []
RecipeData = []
def get_saved_recipes(conn):
    cur = conn.cursor()
    cur.execute("SELECT Label, HealthLabels, DietLabels, IngredientLines, DishType, MealType FROM SavedRecipes WHERE Username=?", (Username[0],))                                                                                                                                                                                                                                                                                                                                                                                                                                   
    rows = cur.fetchall()
    return rows

def check_recipe(conn,username,label):
    cur = conn.cursor()
    cur.execute("SELECT Label FROM SavedRecipes WHERE Username=?", (username,))
    row = cur.fetchall()
    for i in row:
        if str(i[0]) == label:
            return True
    return False

def create_recipe(conn, data):
    sql = ''' INSERT INTO SavedRecipes(Username,Label,HealthLabels,DietLabels,IngredientLines,DishType,MealType)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

def check_username(conn,username):
    cur = conn.cursor()
    cur.execute("SELECT Username FROM User")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == username:
            return True
    return False

def check_password(conn,username,password):
    cur = conn.cursor()
    cur.execute("SELECT Password FROM User WHERE Username=?", (username,))
    row = cur.fetchall()
    if row[0][0] == password:
        return True
    else:
        return False

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

class FloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)
        ActiveButtons.append(self.ids.Continue_Button)

    def OpenSavedPress(self):
        if self.ids.ChooseBackground.x == 0:
            for i in ActiveButtons:
                i.background_normal = i.background_disabled_normal
            ActiveButtons.clear()
            ActiveButtons.append(self.ids.ReturnChoose2_Button)
            self.ids.SavedBackground.x += -1800
            self.ids.ReturnChoose2_Button.x += -1800
            self.ids.SavedList.parent.x += -1800
            Window.set_system_cursor('arrow')
            anim = Animation(pos=(self.ids.ChooseBackground.x + 750, self.ids.ChooseBackground.y), t='in_out_quad')
            anim.start(self.ids.ChooseBackground)
            anim2 = Animation(pos=(self.ids.OpenSaved_Button.x + 750, self.ids.OpenSaved_Button.y), t='in_out_quad')
            anim2.start(self.ids.OpenSaved_Button)
            anim4 = Animation(pos=(self.ids.StartNew_Button.x + 750, self.ids.StartNew_Button.y), t='in_out_quad')
            anim4.start(self.ids.StartNew_Button)
            anim5 = Animation(pos=(self.ids.ReturnLogin_Button.x + 750, self.ids.ReturnLogin_Button.y), t='in_out_quad')
            anim5.start(self.ids.ReturnLogin_Button)
            
            anim = Animation(pos=(self.ids.SavedBackground.x + 900, self.ids.SavedBackground.y), t='in_out_quad')
            anim.start(self.ids.SavedBackground)
            anim2 = Animation(pos=(self.ids.ReturnChoose2_Button.x + 900, self.ids.ReturnChoose2_Button.y), t='in_out_quad')
            anim2.start(self.ids.ReturnChoose2_Button)
            anim4 = Animation(pos=(self.ids.SavedList.parent.x + 900, self.ids.SavedList.parent.y), t='in_out_quad')
            anim4.start(self.ids.SavedList.parent)
            conn = create_connection(r"FoodForYou.db")
            self.ids.SavedList.clear_widgets()
            self.ids.SavedList.height = 45
            with conn:
                recipes = get_saved_recipes(conn)
                h=45
                for i in recipes:
                    self.ids.SavedList.height = h
                    button = HoverButton(text=i[0],pos=(11,h-45),size=(132,45),background_disabled_normal='SavedButton.png',background_normal='SavedButton.png',background_down='SavedButtonA.png',text_size=(132,45),valign="middle",halign="center",bold=True,font_size=12)
                    button.bind(on_press = partial(self.ViewSavedRecipe,i))
                    self.ids.SavedList.add_widget(button)
                    h += 60
            
    def ViewSavedRecipe(self,recipe,a):
        if self.ids.SavedBackground.x == 0:
            for i in a.parent.children:
                i.background_normal = 'SavedButton.png'
            a.background_normal='SavedButtonA.png'
            self.ids.SavedBackground.clear_widgets()

            Title = Label(text=recipe[0],color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=20,pos=(520,515),text_size=(390,200),halign='center')
            self.ids.SavedBackground.add_widget(Title)
            
            if recipe[2] != "Diet Labels:\n":
                diet = Label(text=recipe[2],color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=12,pos=(460,230),text_size=(400,112),valign="top")
                self.ids.SavedBackground.add_widget(diet)
                
            health = Label(text=recipe[1],color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=12,pos=(460,300),text_size=(400,200),valign="top")
            self.ids.SavedBackground.add_widget(health)
            
            ingredient = Label(text=recipe[3],color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=16,pos=(540,150),text_size=(560,200),valign="top")
            self.ids.SavedBackground.add_widget(ingredient)
            
            meal = Label(text=recipe[5],color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=12,pos=(785,300),text_size=(150,200),valign="top")
            self.ids.SavedBackground.add_widget(meal)

            dish = Label(text=recipe[4],color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=12,pos=(755,230),text_size=(90,200),valign="top")
            self.ids.SavedBackground.add_widget(dish)


    def ReturnChoosePress2(self):
        if self.ids.SavedBackground.x == 0:
            for i in self.ids.SavedList.children:
                i.background_normal = 'SavedButton.png'
            for i in ActiveButtons:
                    i.background_normal = i.background_disabled_normal
            ActiveButtons.clear()
            self.ids.SavedBackground.clear_widgets()
            ActiveButtons.append(self.ids.OpenSaved_Button)
            ActiveButtons.append(self.ids.StartNew_Button)
            ActiveButtons.append(self.ids.ReturnLogin_Button)
            self.ids.ChooseBackground.x += -1500
            self.ids.OpenSaved_Button.x += -1500
            self.ids.StartNew_Button.x += -1500
            self.ids.ReturnLogin_Button.x += -1500
            Window.set_system_cursor('arrow')
            anim = Animation(pos=(self.ids.SavedBackground.x + 900, self.ids.SavedBackground.y), t='in_out_quad')
            anim.start(self.ids.SavedBackground)
            anim2 = Animation(pos=(self.ids.ReturnChoose2_Button.x + 900, self.ids.ReturnChoose2_Button.y), t='in_out_quad')
            anim2.start(self.ids.ReturnChoose2_Button)
            anim4 = Animation(pos=(self.ids.SavedList.parent.x + 900, self.ids.SavedList.parent.y), t='in_out_quad')
            anim4.start(self.ids.SavedList.parent)
            
            anim = Animation(pos=(self.ids.ChooseBackground.x + 750, self.ids.ChooseBackground.y), t='in_out_quad')
            anim.start(self.ids.ChooseBackground)
            anim2 = Animation(pos=(self.ids.OpenSaved_Button.x + 750, self.ids.OpenSaved_Button.y), t='in_out_quad')
            anim2.start(self.ids.OpenSaved_Button)
            anim4 = Animation(pos=(self.ids.StartNew_Button.x + 750, self.ids.StartNew_Button.y), t='in_out_quad')
            anim4.start(self.ids.StartNew_Button)
            anim5 = Animation(pos=(self.ids.ReturnLogin_Button.x + 750, self.ids.ReturnLogin_Button.y), t='in_out_quad')
            anim5.start(self.ids.ReturnLogin_Button)



    def SavePress(self):
        if self.ids.ViewBackground.x == 0:
            self.ids.SavedMessage.color = 1,1,1,0
            self.ids.AlreadySavedMessage.color = 1,1,1,0
            label = RecipeData[0]
            healthLabels = RecipeData[2]
            dietLabels = RecipeData[3]
            ingredientLines = RecipeData[4]
            dishType = RecipeData[5]
            mealType = RecipeData[6]
            username = Username[0]
            dietLabels = "Diet Labels:\n"+", ".join(dietLabels)
            healthLabels = "Health Labels:\n"+", ".join(healthLabels)
            ingredientLines = "Ingredients:\n"+",\n".join(ingredientLines)
            mealType = "Meal Type:\n"+", ".join(mealType)
            dishType = "Dish Type:\n"+", ".join(dishType)
            data = (username,label,healthLabels,dietLabels,ingredientLines,dishType,mealType)
            conn = create_connection(r"FoodForYou.db")
            with conn:
                status = check_recipe(conn,username,label)
                if status == False:
                    create_recipe(conn,data)
                    self.ids.SavedMessage.color = 1,1,1,1
                else:
                    self.ids.AlreadySavedMessage.color = 1,1,1,1


    def ViewRecipe(self,label,image,healthLabels,dietLabels,ingredientLines,dishType,mealType,b):
        if self.ids.SearchBackground.x == 0:
            RecipeData.append(label)
            RecipeData.append(image)
            RecipeData.append(healthLabels)
            RecipeData.append(dietLabels)
            RecipeData.append(ingredientLines)
            RecipeData.append(dishType)
            RecipeData.append(mealType)
            self.ids.NoResultError.color = 1,1,1,0
            for i in ActiveButtons:
                    i.background_normal = i.background_disabled_normal
            ActiveButtons.clear()
            ActiveButtons.append(self.ids.Save_Button)
            ActiveButtons.append(self.ids.ReturnSearch_Button)
            self.ids.ViewBackground.x += -1800
            self.ids.ReturnSearch_Button.x += -1800
            self.ids.Save_Button.x += -1800
            self.ids.SearchInput.disabled = True
            self.ids.HealthInput.disabled = True
            self.ids.DietInput.disabled = True
            self.ids.MealTypeInput.disabled = True
            self.ids.DishTypeInput.disabled = True
            anim = Animation(pos=(self.ids.SearchBackground.x + 900, self.ids.SearchBackground.y), t='in_out_quad')
            anim.start(self.ids.SearchBackground)
            anim2 = Animation(pos=(self.ids.ReturnChoose_Button.x + 900, self.ids.ReturnChoose_Button.y), t='in_out_quad')
            anim2.start(self.ids.ReturnChoose_Button)
            anim4 = Animation(pos=(self.ids.SearchInput.x + 900, self.ids.SearchInput.y), t='in_out_quad')
            anim4.start(self.ids.SearchInput)
            anim5 = Animation(pos=(self.ids.HealthInput.x + 900, self.ids.HealthInput.y), t='in_out_quad')
            anim5.start(self.ids.HealthInput)
            anim6 = Animation(pos=(self.ids.DietInput.x + 900, self.ids.DietInput.y), t='in_out_quad')
            anim6.start(self.ids.DietInput)
            anim7 = Animation(pos=(self.ids.MealTypeInput.x + 900, self.ids.MealTypeInput.y), t='in_out_quad')
            anim7.start(self.ids.MealTypeInput)
            anim8 = Animation(pos=(self.ids.DishTypeInput.x + 900, self.ids.DishTypeInput.y), t='in_out_quad')
            anim8.start(self.ids.DishTypeInput)
            anim9 = Animation(pos=(self.ids.RecipeList.parent.x + 900, self.ids.RecipeList.parent.y), t='in_out_quad')
            anim9.start(self.ids.RecipeList.parent)

            anim = Animation(pos=(self.ids.ViewBackground.x + 900, self.ids.ViewBackground.y), t='in_out_quad')
            anim.start(self.ids.ViewBackground)
            anim2 = Animation(pos=(self.ids.ReturnSearch_Button.x + 900, self.ids.ReturnSearch_Button.y), t='in_out_quad')
            anim2.start(self.ids.ReturnSearch_Button)
            anim4 = Animation(pos=(self.ids.Save_Button.x + 900, self.ids.Save_Button.y), t='in_out_quad')
            anim4.start(self.ids.Save_Button)
            thumbnail = AsyncImage(source=image,size=(150,150),pos=(-670,310))
            self.ids.ViewBackground.add_widget(thumbnail)
            anim4 = Animation(pos=(thumbnail.x + 900, thumbnail.y), t='in_out_quad')
            anim4.start(thumbnail)
            Title = Label(text=label,color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=16,pos=(-438,525),text_size=(350,200),halign='center')
            self.ids.ViewBackground.add_widget(Title)
            anim4 = Animation(pos=(Title.x + 900, Title.y), t='in_out_quad')
            anim4.start(Title)
            dietLabels = "Diet Labels:\n"+", ".join(dietLabels)
            healthLabels = "Health Labels:\n"+", ".join(healthLabels)
            ingredients = "Ingredients:\n"+",\n".join(ingredientLines)
            mealType = "Meal Type:\n"+", ".join(mealType)
            dishType = "Dish Type:\n"+", ".join(dishType)
            if dietLabels != "Diet Labels:\n":
                diet = Label(text=dietLabels,color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=12,pos=(-360,240),text_size=(400,112),valign="top")
                self.ids.ViewBackground.add_widget(diet)
                anim4 = Animation(pos=(diet.x + 900, diet.y), t='in_out_quad')
                anim4.start(diet)
            health = Label(text=healthLabels,color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=12,pos=(-360,310),text_size=(400,200),valign="top")
            self.ids.ViewBackground.add_widget(health)
            anim4 = Animation(pos=(health.x + 900, health.y), t='in_out_quad')
            anim4.start(health)
            ingredient = Label(text=ingredients,color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=16,pos=(-520,160),text_size=(400,200),valign="top")
            self.ids.ViewBackground.add_widget(ingredient)
            anim4 = Animation(pos=(ingredient.x + 900, ingredient.y), t='in_out_quad')
            anim4.start(ingredient)
            meal = Label(text=mealType,color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=12,pos=(-255,160),text_size=(150,200),valign="top")
            self.ids.ViewBackground.add_widget(meal)
            anim4 = Animation(pos=(meal.x + 900, meal.y), t='in_out_quad')
            anim4.start(meal)
            dish = Label(text=dishType,color=(0,0,0,1),font_name='Comfortaa-VariableFont_wght.ttf',font_size=12,pos=(-255,130),text_size=(150,200),valign="top")
            self.ids.ViewBackground.add_widget(dish)
            anim4 = Animation(pos=(dish.x + 900, dish.y), t='in_out_quad')
            anim4.start(dish)

            
            

    def ReturnSearchPress(self):
        if self.ids.ViewBackground.x == 0:
            self.ids.SavedMessage.color = 1,1,1,0
            self.ids.AlreadySavedMessage.color = 1,1,1,0
            RecipeData.clear()
            for i in ActiveButtons:
                i.background_normal = i.background_disabled_normal
            self.ids.ViewBackground.clear_widgets()
            ActiveButtons.clear()
            ActiveButtons.append(self.ids.ReturnChoose_Button)
            self.ids.SearchBackground.x += -1800
            self.ids.ReturnChoose_Button.x += -1800
            self.ids.SearchInput.x += -1800
            self.ids.HealthInput.x += -1800
            self.ids.DietInput.x += -1800
            self.ids.MealTypeInput.x += -1800
            self.ids.DishTypeInput.x += -1800
            self.ids.RecipeList.parent.x += -1800
            Window.set_system_cursor('arrow')
            self.ids.SearchInput.disabled = False
            self.ids.HealthInput.disabled = False
            self.ids.DietInput.disabled = False
            self.ids.MealTypeInput.disabled = False
            self.ids.DishTypeInput.disabled = False
            anim = Animation(pos=(self.ids.ViewBackground.x + 900, self.ids.ViewBackground.y), t='in_out_quad')
            anim.start(self.ids.ViewBackground)
            anim2 = Animation(pos=(self.ids.ReturnSearch_Button.x + 900, self.ids.ReturnSearch_Button.y), t='in_out_quad')
            anim2.start(self.ids.ReturnSearch_Button)
            anim4 = Animation(pos=(self.ids.Save_Button.x + 900, self.ids.Save_Button.y), t='in_out_quad')
            anim4.start(self.ids.Save_Button)

            anim = Animation(pos=(self.ids.SearchBackground.x + 900, self.ids.SearchBackground.y), t='in_out_quad')
            anim.start(self.ids.SearchBackground)
            anim2 = Animation(pos=(self.ids.ReturnChoose_Button.x + 900, self.ids.ReturnChoose_Button.y), t='in_out_quad')
            anim2.start(self.ids.ReturnChoose_Button)
            anim4 = Animation(pos=(self.ids.SearchInput.x + 900, self.ids.SearchInput.y), t='in_out_quad')
            anim4.start(self.ids.SearchInput)
            anim5 = Animation(pos=(self.ids.HealthInput.x + 900, self.ids.HealthInput.y), t='in_out_quad')
            anim5.start(self.ids.HealthInput)
            anim6 = Animation(pos=(self.ids.DietInput.x + 900, self.ids.DietInput.y), t='in_out_quad')
            anim6.start(self.ids.DietInput)
            anim7 = Animation(pos=(self.ids.MealTypeInput.x + 900, self.ids.MealTypeInput.y), t='in_out_quad')
            anim7.start(self.ids.MealTypeInput)
            anim8 = Animation(pos=(self.ids.DishTypeInput.x + 900, self.ids.DishTypeInput.y), t='in_out_quad')
            anim8.start(self.ids.DishTypeInput)
            anim9 = Animation(pos=(self.ids.RecipeList.parent.x + 900, self.ids.RecipeList.parent.y), t='in_out_quad')
            anim9.start(self.ids.RecipeList.parent)


    def StartSearch(self):
        self.ids.RecipeList.clear_widgets()
        self.ids.RecipeList.height = 207
        Search = self.ids.SearchInput.text
        Health = self.ids.HealthInput.text
        Diet = self.ids.DietInput.text
        MealType = self.ids.MealTypeInput.text
        DishType = self.ids.DishTypeInput.text
        self.ids.NoResultError.color = 1,1,1,0
        if Search != "":
            MealType_status = False
            DishType_status = False
            Diet_status = False
            Health_status = False
            Error = False
            if DishType != "":
                DishType = DishType.replace(" ","")
                DishType = DishType.lower()
                if "," in DishType:
                    DishType = DishType.split(",")
                else:
                    DishType = DishType.split()
                num = 0
                for i in DishType:
                    DishType[num] = i[0].upper() + i[1:]
                    num += 1
                DishType_List = ["Bread","Cereals","Desserts","Drinks","Pancake","Preps","Preserve","Salad","Sandwiches","Soup","Starter","Sweets"]
                DishType_status = True
                for method in DishType:
                    if method in DishType_List:
                        pass
                    else:
                        Error = True
            if MealType != "":
                MealType = MealType.replace(" ","")
                MealType = MealType.lower()
                if "," in MealType:
                    MealType = MealType.split(",")
                else:
                    MealType = MealType.split()
                num = 0
                for i in MealType:
                    MealType[num] = i[0].upper() + i[1:]
                    num += 1
                MealType_List = ["Breakfast","Dinner","Lunch","Snack","Teatime"]
                MealType_status = True
                for method in MealType:
                    if method in MealType_List:
                        pass
                    else:
                        Error = True
            if Health != "":
                Health = Health.replace(" ","")
                Health = Health.lower()
                if "," in Health:
                    Health = Health.split(",")
                else:
                    Health = Health.split()
                Health_List = ["alcohol-cocktail","alcohol-free","celery-free","crustacean-free","dairy-free","egg-free","fish-free","fodmap-free","gluten-free","immuno-supportive","keto-friendly","kidney-friendly","kosher","low-fat-abs","low-potassium","low-sugar","lupine-free","Mediterranean","mollusk-free","mustard-free","no-oil-added","paleo","peanut-free","pescatarian","pork-free","red-meat-free","sesame-free","shellfish-free","soy-free","sugar-conscious","sulfite-free","tree-nut-free","vegan","vegetarian","wheat-free"]
                Health_status = True
                for method in Health:
                    if method in Health_List:
                        pass
                    else:
                        Error = True
            if Diet != "":
                Diet = Diet.replace(" ","")
                Diet = Diet.lower()
                if "," in Diet:
                    Diet = Diet.split(",")
                else:
                    Diet = Diet.split()
                Diet_List = ["balanced","high-fiber","high-protein","low-carb","low-fat","low-sodium"]
                Diet_status = True
                for method in Diet:
                    if method in Diet_List:
                        pass
                    else:
                        Error = True
            if Error == False:
                app_id = "" # Add id
                app_key = "" # Add key
                if DishType_status == True:
                    if MealType_status == True:
                        if Health_status == True:
                            if Diet_status == True:
                                Health = "&health=".join(Health)
                                Diet = "&diet=".join(Diet)
                                MealType = "&mealType=".join(MealType)
                                DishType = "&dishType=".join(DishType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&mealType={MealType}&dishType={DishType}&health={Health}&diet={Diet}&imageSize=THUMBNAIL').json()
                            else:
                                Health = "&health=".join(Health)
                                MealType = "&mealType=".join(MealType)
                                DishType = "&dishType=".join(DishType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&mealType={MealType}&dishType={DishType}&health={Health}&imageSize=THUMBNAIL').json()
                        else:
                            if Diet_status == True:
                                Diet = "&diet=".join(Diet)
                                MealType = "&mealType=".join(MealType)
                                DishType = "&dishType=".join(DishType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&mealType={MealType}&dishType={DishType}&diet={Diet}&imageSize=THUMBNAIL').json()
                            else:
                                MealType = "&mealType=".join(MealType)
                                DishType = "&dishType=".join(DishType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&mealType={MealType}&dishType={DishType}&imageSize=THUMBNAIL').json()
                    else:
                        if Health_status == True:
                            if Diet_status == True:
                                Health = "&health=".join(Health)
                                Diet = "&diet=".join(Diet)
                                DishType = "&dishType=".join(DishType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&dishType={DishType}&health={Health}&diet={Diet}&imageSize=THUMBNAIL').json()
                            else:
                                Health = "&health=".join(Health)
                                DishType = "&dishType=".join(DishType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&dishType={DishType}&health={Health}&imageSize=THUMBNAIL').json()
                        else:
                            if Diet_status == True:
                                Diet = "&diet=".join(Diet)
                                DishType = "&dishType=".join(DishType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&dishType={DishType}&diet={Diet}&imageSize=THUMBNAIL').json()
                            else:
                                DishType = "&dishType=".join(DishType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&dishType={DishType}&imageSize=THUMBNAIL').json()
                else:
                    if MealType_status == True:
                        if Health_status == True:
                            if Diet_status == True:
                                Health = "&health=".join(Health)
                                Diet = "&diet=".join(Diet)
                                MealType = "&mealType=".join(MealType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&mealType={MealType}&health={Health}&diet={Diet}&imageSize=THUMBNAIL').json()
                            else:
                                Health = "&health=".join(Health)
                                MealType = "&mealType=".join(MealType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&mealType={MealType}&health={Health}&imageSize=THUMBNAIL').json()
                        else:
                            if Diet_status == True:
                                Diet = "&diet=".join(Diet)
                                MealType = "&mealType=".join(MealType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&mealType={MealType}&diet={Diet}&imageSize=THUMBNAIL').json()
                            else:
                                MealType = "&mealType=".join(MealType)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&mealType={MealType}&imageSize=THUMBNAIL').json()
                    else:
                        if Health_status == True:
                            if Diet_status == True:
                                Health = "&health=".join(Health)
                                Diet = "&diet=".join(Diet)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&health={Health}&diet={Diet}&imageSize=THUMBNAIL').json()
                            else:
                                Health = "&health=".join(Health)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&health={Health}&imageSize=THUMBNAIL').json()
                        else:
                            if Diet_status == True:
                                Diet = "&diet=".join(Diet)
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&diet={Diet}&imageSize=THUMBNAIL').json()
                            else:
                                data = requests.get(f'https://api.edamam.com/api/recipes/v2?type=public&q={Search}&app_id={app_id}&app_key={app_key}&imageSize=THUMBNAIL').json() 
                if data['hits']:
                    h = 107
                    for i in data['hits']:
                        self.ids.RecipeList.height = h
                        background = Image(source="RecipeBackground.png",size=(396,107),pos=(0,h-107))
                        self.ids.RecipeList.add_widget(background)
                        thumbnail = AsyncImage(source=i['recipe']['image'],size=(100,100),pos=(10,h-103.5))
                        self.ids.RecipeList.add_widget(thumbnail)
                        label = TextInput(text=i['recipe']['label'],background_color=(1,1,1,0),font_name='Comfortaa-VariableFont_wght.ttf',font_size=16,pos=(120,h-103.5),multiline=True,disabled=True,disabled_foreground_color=(0,0,0,1),size=(200,100))
                        self.ids.RecipeList.add_widget(label)
                        button = HoverButton(pos=(293,h-103.5),size=(100,35),background_disabled_normal='ViewRecipe.png',background_normal='ViewRecipe.png',background_down='ViewRecipeA.png')
                        if 'dishType' in i['recipe']:
                            dishType = i['recipe']['dishType']
                        else:
                            dishType = []
                        button.bind(on_press = partial(self.ViewRecipe,i['recipe']['label'],i['recipe']['image'],i['recipe']['healthLabels'],i['recipe']['dietLabels'],i['recipe']['ingredientLines'],dishType,i['recipe']['mealType']))
                        self.ids.RecipeList.add_widget(button)
                        h += 120
                else:
                    self.ids.NoResultError.color = 1,1,1,1
            else:
                self.ids.NoResultError.color = 1,1,1,1
        else:
            self.ids.NoResultError.color = 1,1,1,1


    def StartNewPress(self):
        if self.ids.ChooseBackground.x == 0:
            for i in ActiveButtons:
                i.background_normal = i.background_disabled_normal
            ActiveButtons.clear()
            ActiveButtons.append(self.ids.ReturnChoose_Button)
            self.ids.SearchBackground.x += -1800
            self.ids.ReturnChoose_Button.x += -1800
            self.ids.SearchInput.x += -1800
            self.ids.HealthInput.x += -1800
            self.ids.DietInput.x += -1800
            self.ids.MealTypeInput.x += -1800
            self.ids.DishTypeInput.x += -1800
            self.ids.RecipeList.parent.x += -1800
            Window.set_system_cursor('arrow')
            self.ids.SearchInput.disabled = False
            self.ids.HealthInput.disabled = False
            self.ids.DietInput.disabled = False
            self.ids.MealTypeInput.disabled = False
            self.ids.DishTypeInput.disabled = False
            anim = Animation(pos=(self.ids.ChooseBackground.x + 750, self.ids.ChooseBackground.y), t='in_out_quad')
            anim.start(self.ids.ChooseBackground)
            anim2 = Animation(pos=(self.ids.OpenSaved_Button.x + 750, self.ids.OpenSaved_Button.y), t='in_out_quad')
            anim2.start(self.ids.OpenSaved_Button)
            anim4 = Animation(pos=(self.ids.StartNew_Button.x + 750, self.ids.StartNew_Button.y), t='in_out_quad')
            anim4.start(self.ids.StartNew_Button)
            anim5 = Animation(pos=(self.ids.ReturnLogin_Button.x + 750, self.ids.ReturnLogin_Button.y), t='in_out_quad')
            anim5.start(self.ids.ReturnLogin_Button)

            anim = Animation(pos=(self.ids.SearchBackground.x + 900, self.ids.SearchBackground.y), t='in_out_quad')
            anim.start(self.ids.SearchBackground)
            anim2 = Animation(pos=(self.ids.ReturnChoose_Button.x + 900, self.ids.ReturnChoose_Button.y), t='in_out_quad')
            anim2.start(self.ids.ReturnChoose_Button)
            anim4 = Animation(pos=(self.ids.SearchInput.x + 900, self.ids.SearchInput.y), t='in_out_quad')
            anim4.start(self.ids.SearchInput)
            anim5 = Animation(pos=(self.ids.HealthInput.x + 900, self.ids.HealthInput.y), t='in_out_quad')
            anim5.start(self.ids.HealthInput)
            anim6 = Animation(pos=(self.ids.DietInput.x + 900, self.ids.DietInput.y), t='in_out_quad')
            anim6.start(self.ids.DietInput)
            anim7 = Animation(pos=(self.ids.MealTypeInput.x + 900, self.ids.MealTypeInput.y), t='in_out_quad')
            anim7.start(self.ids.MealTypeInput)
            anim8 = Animation(pos=(self.ids.DishTypeInput.x + 900, self.ids.DishTypeInput.y), t='in_out_quad')
            anim8.start(self.ids.DishTypeInput)
            anim9 = Animation(pos=(self.ids.RecipeList.parent.x + 900, self.ids.RecipeList.parent.y), t='in_out_quad')
            anim9.start(self.ids.RecipeList.parent)

    def ReturnChoosePress(self):
        if self.ids.SearchBackground.x == 0:
            self.ids.NoResultError.color = 1,1,1,0
            for i in ActiveButtons:
                    i.background_normal = i.background_disabled_normal
            ActiveButtons.clear()
            ActiveButtons.append(self.ids.OpenSaved_Button)
            ActiveButtons.append(self.ids.StartNew_Button)
            ActiveButtons.append(self.ids.ReturnLogin_Button)
            self.ids.ChooseBackground.x += -1500
            self.ids.OpenSaved_Button.x += -1500
            self.ids.StartNew_Button.x += -1500
            self.ids.ReturnLogin_Button.x += -1500
            Window.set_system_cursor('arrow')
            self.ids.SearchInput.disabled = True
            self.ids.HealthInput.disabled = True
            self.ids.DietInput.disabled = True
            self.ids.MealTypeInput.disabled = True
            self.ids.DishTypeInput.disabled = True
            anim = Animation(pos=(self.ids.SearchBackground.x + 900, self.ids.SearchBackground.y), t='in_out_quad')
            anim.start(self.ids.SearchBackground)
            anim2 = Animation(pos=(self.ids.ReturnChoose_Button.x + 900, self.ids.ReturnChoose_Button.y), t='in_out_quad')
            anim2.start(self.ids.ReturnChoose_Button)
            anim4 = Animation(pos=(self.ids.SearchInput.x + 900, self.ids.SearchInput.y), t='in_out_quad')
            anim4.start(self.ids.SearchInput)
            anim5 = Animation(pos=(self.ids.HealthInput.x + 900, self.ids.HealthInput.y), t='in_out_quad')
            anim5.start(self.ids.HealthInput)
            anim6 = Animation(pos=(self.ids.DietInput.x + 900, self.ids.DietInput.y), t='in_out_quad')
            anim6.start(self.ids.DietInput)
            anim7 = Animation(pos=(self.ids.MealTypeInput.x + 900, self.ids.MealTypeInput.y), t='in_out_quad')
            anim7.start(self.ids.MealTypeInput)
            anim8 = Animation(pos=(self.ids.DishTypeInput.x + 900, self.ids.DishTypeInput.y), t='in_out_quad')
            anim8.start(self.ids.DishTypeInput)
            anim9 = Animation(pos=(self.ids.RecipeList.parent.x + 900, self.ids.RecipeList.parent.y), t='in_out_quad')
            anim9.start(self.ids.RecipeList.parent)

            anim = Animation(pos=(self.ids.ChooseBackground.x + 750, self.ids.ChooseBackground.y), t='in_out_quad')
            anim.start(self.ids.ChooseBackground)
            anim2 = Animation(pos=(self.ids.OpenSaved_Button.x + 750, self.ids.OpenSaved_Button.y), t='in_out_quad')
            anim2.start(self.ids.OpenSaved_Button)
            anim4 = Animation(pos=(self.ids.StartNew_Button.x + 750, self.ids.StartNew_Button.y), t='in_out_quad')
            anim4.start(self.ids.StartNew_Button)
            anim5 = Animation(pos=(self.ids.ReturnLogin_Button.x + 750, self.ids.ReturnLogin_Button.y), t='in_out_quad')
            anim5.start(self.ids.ReturnLogin_Button)



    def ReturnLoginPress(self):
        if self.ids.ChooseBackground.x == 0:
            for i in ActiveButtons:
                i.background_normal = i.background_disabled_normal
            ActiveButtons.clear()
            Username.clear()
            self.ids.RecipeList.clear_widgets()
            self.ids.RecipeList.height = 207
            ActiveButtons.append(self.ids.Continue_Button)
            self.ids.LoginBackground.x += -1500
            self.ids.UsernameInput.x += -1500
            self.ids.PasswordInput.x += -1500
            self.ids.Continue_Button.x += -1500
            Window.set_system_cursor('arrow')
            self.ids.UsernameInput.text = ''
            self.ids.PasswordInput.text = ''
            self.ids.SearchInput.text = ''
            self.ids.HealthInput.text = ''
            self.ids.DietInput.text = ''
            self.ids.MealTypeInput.text = ''
            self.ids.DishTypeInput.text = ''
            self.ids.UsernameInput.disabled = False
            self.ids.PasswordInput.disabled = False
            anim = Animation(pos=(self.ids.ChooseBackground.x + 750, self.ids.ChooseBackground.y), t='in_out_quad')
            anim.start(self.ids.ChooseBackground)
            anim2 = Animation(pos=(self.ids.OpenSaved_Button.x + 750, self.ids.OpenSaved_Button.y), t='in_out_quad')
            anim2.start(self.ids.OpenSaved_Button)
            anim4 = Animation(pos=(self.ids.StartNew_Button.x + 750, self.ids.StartNew_Button.y), t='in_out_quad')
            anim4.start(self.ids.StartNew_Button)
            anim5 = Animation(pos=(self.ids.ReturnLogin_Button.x + 750, self.ids.ReturnLogin_Button.y), t='in_out_quad')
            anim5.start(self.ids.ReturnLogin_Button)

            anim = Animation(pos=(self.ids.LoginBackground.x + 750, self.ids.LoginBackground.y), t='in_out_quad')
            anim.start(self.ids.LoginBackground)
            anim2 = Animation(pos=(self.ids.Continue_Button.x + 750, self.ids.Continue_Button.y), t='in_out_quad')
            anim2.start(self.ids.Continue_Button)
            anim4 = Animation(pos=(self.ids.UsernameInput.x + 750, self.ids.UsernameInput.y), t='in_out_quad')
            anim4.start(self.ids.UsernameInput)
            anim5 = Animation(pos=(self.ids.PasswordInput.x + 750, self.ids.PasswordInput.y), t='in_out_quad')
            anim5.start(self.ids.PasswordInput)

    def ContinuePress(self):
        if self.ids.LoginBackground.x == 0:
            username = self.ids.UsernameInput.text
            password = self.ids.PasswordInput.text
            password = hashlib.sha256(password.encode())
            password = password.hexdigest()
            conn = create_connection(r"FoodForYou.db")
            self.ids.LoginError.color = 1,1,1,0
            with conn:
                username_status = check_username(conn,username)
                if username_status == True:
                    password_status = check_password(conn,username,password)
                    if password_status == True:
                        Username.append(username)
                        for i in ActiveButtons:
                            i.background_normal = i.background_disabled_normal
                        ActiveButtons.clear()
                        ActiveButtons.append(self.ids.OpenSaved_Button)
                        ActiveButtons.append(self.ids.StartNew_Button)
                        ActiveButtons.append(self.ids.ReturnLogin_Button)
                        self.ids.ChooseBackground.x += -1500
                        self.ids.OpenSaved_Button.x += -1500
                        self.ids.StartNew_Button.x += -1500
                        self.ids.ReturnLogin_Button.x += -1500
                        Window.set_system_cursor('arrow')
                        self.ids.UsernameInput.disabled = True
                        self.ids.PasswordInput.disabled = True
                        anim = Animation(pos=(self.ids.LoginBackground.x + 750, self.ids.LoginBackground.y), t='in_out_quad')
                        anim.start(self.ids.LoginBackground)
                        anim2 = Animation(pos=(self.ids.Continue_Button.x + 750, self.ids.Continue_Button.y), t='in_out_quad')
                        anim2.start(self.ids.Continue_Button)
                        anim4 = Animation(pos=(self.ids.UsernameInput.x + 750, self.ids.UsernameInput.y), t='in_out_quad')
                        anim4.start(self.ids.UsernameInput)
                        anim5 = Animation(pos=(self.ids.PasswordInput.x + 750, self.ids.PasswordInput.y), t='in_out_quad')
                        anim5.start(self.ids.PasswordInput)

                        anim = Animation(pos=(self.ids.ChooseBackground.x + 750, self.ids.ChooseBackground.y), t='in_out_quad')
                        anim.start(self.ids.ChooseBackground)
                        anim2 = Animation(pos=(self.ids.OpenSaved_Button.x + 750, self.ids.OpenSaved_Button.y), t='in_out_quad')
                        anim2.start(self.ids.OpenSaved_Button)
                        anim4 = Animation(pos=(self.ids.StartNew_Button.x + 750, self.ids.StartNew_Button.y), t='in_out_quad')
                        anim4.start(self.ids.StartNew_Button)
                        anim5 = Animation(pos=(self.ids.ReturnLogin_Button.x + 750, self.ids.ReturnLogin_Button.y), t='in_out_quad')
                        anim5.start(self.ids.ReturnLogin_Button)
                    else:
                        self.ids.LoginError.color = 1,1,1,1
                else:
                    self.ids.LoginError.color = 1,1,1,1

    

class HoverButton(Button):
    def __init__(self, **kwargs):
        super(HoverButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        if self.collide_point(*pos):
            Clock.schedule_once(self.mouse_enter_css, 0)
        else:
            Clock.schedule_once(self.mouse_leave_css, 0)

    def mouse_leave_css(self, *args):
        if self in ActiveButtons:
            check = 0
            self.background_normal = self.background_disabled_normal
            for i in ActiveButtons:
                if i.background_normal == i.background_disabled_normal:
                    check += 1
            if check == len(ActiveButtons):
                Window.set_system_cursor('arrow')

    def mouse_enter_css(self, *args):
        if self in ActiveButtons:
            self.background_normal = self.background_down
            Window.set_system_cursor('hand')

class Food_For_YouApp(App):
    def build(self):
        return(FloatLayout())

if __name__ == "__main__":

    Food_For_YouApp().run()
