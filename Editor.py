import pygame
import json

XSIZE = 800
YSIZE = 600

#RIGHT CLICK MENU
RightMenuOpen = False
RightMenu = None
OptionList = []
OptionFunctionList = ["createRect"]
MenuSize_X = 200
MenuSize_Y = 100

#LEFT CLICK
left_clicking = False
mouse_rect_offset = [0, 0]

#RECT INTERACTION
chosenRect = None
pressed_cords = [0, 0]
extending = False
extendingRect = None
extendingRect_og_left = None
extendingRect_og_top = None
extendingRect_og_bottom = None
extendingRect_og_right = None
extendingSide = None
RenderList = []

def rightMenu(surface, OptionFuncs):
    global RightMenu
    global ObjectList
    color = (255, 255, 255)
    optionColor = (86, 108, 127)
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    RightMenuSize_X = MenuSize_X
    RightMenuSize_Y = MenuSize_Y
    print(mouse_pos)
    if mouse_x + RightMenuSize_X > XSIZE:
        mouse_x = XSIZE - RightMenuSize_X
    if mouse_y + RightMenuSize_Y > YSIZE:
        mouse_y = YSIZE - RightMenuSize_Y

    RightMenu = pygame.Rect(mouse_x, mouse_y, RightMenuSize_X, RightMenuSize_Y)
    pygame.draw.rect(surface, color, RightMenu)
    RenderList.append({"object": RightMenu, "objectType" : "Rect", "name": "RightMenu", "color": color,
                       "renderPriority": 0})
    for i in OptionFuncs:
        OptionList.append(pygame.Rect(mouse_x, mouse_y, 200, 15))
        n1 = len(OptionList) - 1
        n2 = OptionFuncs.index(i)
        pygame.draw.rect(surface, color, OptionList[n1])
        RenderList.append({"object": OptionList[n1], "objectType" : "Rect", "name" : OptionFuncs[n2]["function"], "color": optionColor,
                       "renderPriority": 1})

def cleanRenderList():
    global RenderList
    new_list = []
    for i in RenderList:
        if (i["objectType"] == "NaN"):
            continue
        else:
            new_list.append(i)
    RenderList = new_list


def deleteRightMenu():
    for i in RenderList:
        if i["objectType"] == "Rect":
            if i["name"] == "RightMenu":
                n = RenderList.index(i)
                RenderList[n] = dict(objectType="NaN")
            if i["name"] in OptionFunctionList:
                n = RenderList.index(i)
                RenderList[n] = dict(objectType="NaN")

def RenderAll(surface):
    global RenderList
    for i in RenderList:
        if i["objectType"] == "Rect":
            pygame.draw.rect(surface, i["color"], i["object"])

def MouseColliders(pos):
    clickables = []
    chosenCollider = None
    for i in RenderList:
        if i["objectType"] == "Rect":
            if i["object"].collidepoint(pos):
                clickables.append(i)
    min = -1
    for i in clickables:
        if int(i["renderPriority"]) > min:
            min = int(i["renderPriority"])
            chosenCollider = i
    if chosenCollider is not None:
        return chosenCollider

def createSimpleRect(surface):
    color = (86, 108, 127)
    mouse_pos = pygame.mouse.get_pos()
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    simple_rect_size = 40
    simple_rect = pygame.Rect(mouse_x, mouse_y, simple_rect_size, simple_rect_size)
    pygame.draw.rect(surface, color, simple_rect)
    RenderList.append({"object": simple_rect, "objectType": "Rect", "name": "simpleRect", "color": color,
                       "renderPriority": 0})

def checkMousePosition():
    clickables = []
    pos = pygame.mouse.get_pos()
    chosenCollider = None
    for i in RenderList:
        if i["objectType"] == "Rect":
            if i["object"].collidepoint(pos):
                clickables.append(i)
    min = -1
    for i in clickables:
        if int(i["renderPriority"]) > min:
            min = int(i["renderPriority"])
            chosenCollider = i
    if chosenCollider is not None and chosenCollider["name"] == "simpleRect":
        if canExtend(pos, chosenCollider["object"]):
            if extendingSide == "left" or extendingSide == "right":
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZEWE))
            else:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_SIZENS))
        else:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    else:
        pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

def canExtend(pos, rect):
    global extendingSide
    if pos[0] < rect.left+5 and pos[0] > rect.left:
        extendingSide = "left"
        return True
    if pos[0] > rect.right-5 and pos[0] < rect.right:
        extendingSide = "right"
        return True
    if pos[1] < rect.top+5 and pos[1] > rect.top:
        extendingSide = "top"
        return True
    if pos[1] > rect.bottom-5 and pos[1] < rect.bottom:
        extendingSide = "bottom"
        return True
    else:
        return False

def extendRect(pos):
    global extendingRect
    global extendingRect_og_left
    global extendingRect_og_top
    global extendingRect_og_right
    global extendingRect_og_bottom
    global extendingSide
    extendingRect_og_left = extendingRect.left
    extendingRect_og_top = extendingRect.top
    extendingRect_og_bottom = extendingRect.bottom
    extendingRect_og_right = extendingRect.right

    if extendingSide == "left":
        extendingRect.left = pos[0] - 5
        extendingRect.width += extendingRect_og_left - extendingRect.left
    if extendingSide == "right":
        extendingRect.width = (pos[0] + 5) - extendingRect.left
    if extendingSide == "top":
        extendingRect.top = pos[1] - 5
        extendingRect.height += extendingRect_og_top - extendingRect.top
    if extendingSide == "bottom":
        extendingRect.height = (pos[1] + 5) - extendingRect.top

def moveRect(pos):
    global pressed_cords
    global chosenRect
    chosenRect.x = pos[0] - mouse_rect_offset[0]
    chosenRect.y = pos[1] - mouse_rect_offset[1]

def exportList():
    global RenderList
    new_list = []
    print(RenderList)
    for i in RenderList:
        current_object = i["object"]

        #Get x, y, w, h
        x = current_object.left
        y = current_object.top
        w = current_object.width
        h = current_object.height

        objectType = i["objectType"]
        name = i["name"]
        color = i["color"]
        renderPriority = i["renderPriority"]
        dict = {"left": x, "top": y, "width": w, "height": h, "objectType": objectType, "name": name,
                "color": color, "renderPriority": renderPriority}
        new_list.append(dict)
    json_list = json.dumps(new_list)

    with open("sample.json", "w") as outfile:
        json.dump(json_list, outfile)
    return json_list


def confLoop():
    global RightMenuOpen
    global extending
    global chosenRect
    global extendingRect
    global pressed_cords
    global left_clicking
    global mouse_rect_offset
    pygame.display.init()
    surface = pygame.display.set_mode((XSIZE, YSIZE), vsync=1)
    isConfig = True
    while isConfig:

        pygame.display.flip()
        surface.fill((0, 0, 0))
        RenderAll(surface)


        #ESPERA EVENTOS
        for event in pygame.event.get():

            #CHECKING MOUSE POSITION
            if not extending:
                checkMousePosition()

            #MENU CLICK DERECHO
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                RightMenu = None
                deleteRightMenu()
                RightMenuOpen = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                OptionList = [{"function" : "createRect"}]
                rightMenu(surface, OptionList)
                RightMenuOpen = True

            #INTERACCIÓN CON MENU DERECHO
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                left_clicking = False
                chosenRect = None
                clicked = MouseColliders(event.pos)
                if RightMenuOpen and (clicked is None or clicked["name"] not in OptionFunctionList):
                    deleteRightMenu()
                elif clicked is not None:
                    createSimpleRect(surface)
                    deleteRightMenu()
                if extending:
                    extending = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                left_clicking = True
                if MouseColliders(event.pos) is not None:
                    collider = MouseColliders(event.pos)
                    if collider["name"] == "simpleRect":
                        chosenRect = collider["object"]
                        if canExtend(event.pos, collider["object"]):
                            extending = True
                            extendingRect = collider["object"]
                        else:
                            mouse_rect_offset[0] = event.pos[0] - chosenRect.x
                            mouse_rect_offset[1] = event.pos[1] - chosenRect.y
                            pressed_cords[0] = event.pos[0]
                            pressed_cords[1] = event.pos[1]

            #MOUSE MOVEMENT
            if event.type == pygame.MOUSEMOTION:
                if left_clicking:
                    if extending:
                        extendRect(event.pos)
                    elif chosenRect is not None:
                        moveRect(event.pos)

            #SALIR
            if event.type == pygame.QUIT:
                cleanRenderList()
                exportList()
                pygame.quit()
                return 0