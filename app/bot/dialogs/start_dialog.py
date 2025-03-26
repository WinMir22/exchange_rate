from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Button, Start
from aiogram_dialog.widgets.text import Const

from app.bot.dialogs.dialogs_states import StartSG, OneRateSG
from app.bot.lexicon.lexicon_ru import lexicon

start_dialog = Dialog(
    Window(
        Const(lexicon["start_command"]),
        Row(
            Start(
                Const(lexicon["exchange_rate_but"]), id="rate_one", state=OneRateSG.main
            ),
            Button(
                Const(lexicon["exchange_rate_but2"]), id="rate_many"
            ),
        ),
        state=StartSG.start
    )
)
