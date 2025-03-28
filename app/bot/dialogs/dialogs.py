from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (
    Row,
    Button,
    Start,
    Cancel,
    ScrollingGroup,
    Back,
    Select,
)
from aiogram_dialog.widgets.text import Const, Format

from app.bot.dialogs.dialog_handlers import check_rate, give_rate
from app.bot.dialogs.dialogs_getters import rate_getter
from app.bot.dialogs.dialogs_states import StartSG, OneRateSG
from app.bot.lexicon.lexicon_ru import lexicon
from app.services.exchange_rate_services.list_of_rates import rates

start_dialog = Dialog(
    Window(
        Const(lexicon["start_command"]),
        Row(
            Start(
                Const(lexicon["exchange_rate_but"]),
                id="rate_one",
                state=OneRateSG.get_rate,
            ),
            Button(Const(lexicon["exchange_rate_but2"]), id="rate_many"),
        ),
        state=StartSG.start,
    )
)


one_rate_dialog = Dialog(
    Window(
        Const(lexicon["exchange_rate_but"]),
        ScrollingGroup(
            Select(
                Format("{item}"),
                id="get_check",
                item_id_getter=lambda x: x,
                items=rates,
                on_click=check_rate,
            ),
            width=4,
            height=10,
            id="all_rates",
        ),
        Cancel(Const(lexicon["back_to_main_menu"])),
        state=OneRateSG.get_rate,
    ),
    Window(
        Const(lexicon["get_code_for_check_state"]),
        ScrollingGroup(
            Select(
                Format("{item}"),
                id="give_check",
                item_id_getter=lambda x: x,
                items=rates,
                on_click=give_rate,
            ),
            width=4,
            height=10,
            id="all_rates",
        ),
        Back(Const(lexicon["back_to_main_menu"])),
        state=OneRateSG.give_rate,
    ),
    Window(
        Format("Эта валюта стоит {result} {value}"),
        Back(Const("Назад")),
        state=OneRateSG.get_result,
        getter=rate_getter,
    ),
)
