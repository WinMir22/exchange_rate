from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Button,
    Start,
    Cancel,
    ScrollingGroup,
    Back,
    Select,
    Column,
)
from aiogram_dialog.widgets.text import Const, Format

from app.bot.dialogs.dialog_handlers import check_rate, favorite_handler, give_rate
from app.bot.dialogs.dialogs_getters import rate_getter, to_usd_getter, rates_getter
from app.bot.dialogs.dialogs_states import StartSG, OneRateSG, FavoriteSG
from app.bot.lexicon.lexicon_ru import lexicon

start_dialog = Dialog(
    Window(
        Const(lexicon["start_command"]),
        Column(
            Start(
                Const(lexicon["exchange_rate_but"]),
                id="rate_one",
                state=OneRateSG.get_rate,
            ),
            Start(Const("Избранное"), id="favorite", state=FavoriteSG.main),
            Button(Const(lexicon["exchange_rate_but2"]), id="rate_many"),
        ),
        state=StartSG.start,
    )
)


favorite_dialog = Dialog(
    Window(
        Const("Избранное"),
        ScrollingGroup(
            Select(
                Format("{item}"),
                id="get_check",
                item_id_getter=lambda x: x,
                items="rates",
                on_click=favorite_handler,
            ),
            width=4,
            height=10,
            id="all_rates",
        ),
        Cancel(Const(lexicon["back_to_main_menu"])),
        state=FavoriteSG.main,
        getter=rates_getter,
    ),
)


one_rate_dialog = Dialog(
    Window(
        Const(lexicon["exchange_rate_but"]),
        ScrollingGroup(
            Select(
                Format("{item}"),
                id="get_check",
                item_id_getter=lambda x: x,
                items="rates",
                on_click=check_rate,
            ),
            width=4,
            height=10,
            id="all_rates",
        ),
        Cancel(Const(lexicon["back_to_main_menu"])),
        state=OneRateSG.get_rate,
        getter=rates_getter,
    ),
    Window(
        Format(lexicon["get_code_for_check_state"]),
        ScrollingGroup(
            Select(
                Format("{item}"),
                id="give_check",
                item_id_getter=lambda x: x,
                items="rates",
                on_click=give_rate,
            ),
            width=4,
            height=10,
            id="all_rates",
        ),
        Back(Const(lexicon["back_to_main_menu"])),
        getter=to_usd_getter,
        state=OneRateSG.give_rate,
    ),
    Window(
        Format("Эта валюта стоит {result} {value}"),
        Back(Const("Назад")),
        state=OneRateSG.get_result,
        getter=rate_getter,
    ),
)
