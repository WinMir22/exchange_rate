"""dialogs from aiogram_dialog"""

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
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
from app.bot.keyboards.texts import BUTTONS_LEXICON
from app.bot.lexicon.lexicon_ru import lexicon

# Main menu
start_dialog = Dialog(
    Window(
        Const(lexicon["start_command"]),
        Column(
            Start(
                Const(BUTTONS_LEXICON["know_rate"]),
                id="rate_one",
                state=OneRateSG.get_rate,
            ),
            Start(Const("Избранное"), id="favorite", state=FavoriteSG.main),
        ),
        state=StartSG.start,
    )
)

# Dialog, which is changes buttons order in the one_rate_dialog.
favorite_dialog = Dialog(
    Window(
        Const("Выберите валюты, которые будут отображаться в начале."),
        ScrollingGroup(
            Select(
                Format("{item}"),
                id="get_check",
                item_id_getter=lambda x: x,  # button id = button text
                items="rates",
                on_click=favorite_handler,
            ),
            width=4,
            height=10,
            id="all_rates",
        ),
        Cancel(Const("Назад")),
        state=FavoriteSG.main,
        getter=rates_getter,
    ),
)


one_rate_dialog = Dialog(
    Window(
        Const(lexicon["first_rate"]),
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
        Cancel(Const("Назад")),
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
        Back(Const("Назад")),
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
