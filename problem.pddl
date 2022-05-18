(define (problem currentEnvironment)
    (:domain camelotdomain)
    (:objects
        alchemyshop - location
        blacksmith - location
        bob - player
        luca - character
        alchemyshop.Chest - furniture
        alchemyshop.Door - entrypoint
        blacksmith.Door - entrypoint
        redkey - item
        alchemyshop.Door.In - position
        alchemyshop.Bar - furniture
        alchemyshop.Bar.Behind - position
        alchemyshop.Bar.Left - position
        alchemyshop.Bar.Center - position
        alchemyshop.Bar.Right - position
        alchemyshop.BackDoor - furniture
        alchemyshop.BackDoor.In - position
        alchemyshop.RightBookcase - furniture
        alchemyshop.LeftBookcase - furniture
        alchemyshop.BookShelf - furniture
        alchemyshop.BookShelf.Left - position
        alchemyshop.BookShelf.Right - position
        alchemyshop.Table - furniture
        alchemyshop.Table.Left - position
        alchemyshop.Table.Right - position
        alchemyshop.Table.FrontLeft - position
        alchemyshop.Table.BackLeft - position
        alchemyshop.Table.FrontRight - position
        alchemyshop.Table.BackRight - position
        alchemyshop.AlchemistTable - furniture
        alchemyshop.AlchemistTable.Left - position
        alchemyshop.AlchemistTable.Right - position
        alchemyshop.AlchemistTable.Center - position
        alchemyshop.Cauldron - furniture
        alchemyshop.Fireplace - furniture
        blacksmith.Door.In - position
        blacksmith.Target - furniture
        blacksmith.Table - furniture
        blacksmith.Table.Left - position
        blacksmith.Table.Right - position
        blacksmith.Table.FrontLeft - position
        blacksmith.Table.FrontRight - position
        blacksmith.Anvil - furniture
        blacksmith.Chest - furniture
        blacksmith.BackDoor - furniture
        blacksmith.BackDoor.In - position
)
    (:init
        (in bob alchemyshop)
        (in luca blacksmith)
        (at luca blacksmith.Door)
        (at bob alchemyshop.Door)
        (at alchemyshop.Chest alchemyshop)
        (adjacent alchemyshop.Door blacksmith.Door)
        (adjacent blacksmith.Door alchemyshop.Door)
        (stored redkey alchemyshop.Chest)
        (can_open alchemyshop.Chest)
        (alive bob)
        (alive luca)
        (at alchemyshop.Door alchemyshop)
        (not is_open alchemyshop.Chest)
        (can_close alchemyshop.Chest)
        (at alchemyshop.Bar alchemyshop)
        (can_open alchemyshop.Bar)
        (not is_open alchemyshop.Bar)
        (can_close alchemyshop.Bar)
        (has_surface alchemyshop.Bar)
        (at alchemyshop.BackDoor alchemyshop)
        (at alchemyshop.RightBookcase alchemyshop)
        (at alchemyshop.LeftBookcase alchemyshop)
        (at alchemyshop.BookShelf alchemyshop)
        (has_surface alchemyshop.BookShelf)
        (at alchemyshop.Table alchemyshop)
        (has_surface alchemyshop.Table)
        (at alchemyshop.AlchemistTable alchemyshop)
        (has_surface alchemyshop.AlchemistTable)
        (at alchemyshop.Cauldron alchemyshop)
        (at alchemyshop.Fireplace alchemyshop)
        (at blacksmith.Door blacksmith)
        (at blacksmith.Target blacksmith)
        (at blacksmith.Table blacksmith)
        (has_surface blacksmith.Table)
        (at blacksmith.Anvil blacksmith)
        (has_surface blacksmith.Anvil)
        (at blacksmith.Chest blacksmith)
        (can_open blacksmith.Chest)
        (not is_open blacksmith.Chest)
        (can_close blacksmith.Chest)
        (at blacksmith.BackDoor blacksmith)
    )
    (:goal
    )
)