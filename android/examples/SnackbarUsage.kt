// Views: styled automatically through snackbarStyle in Theme.Aurora
Snackbar.make(view, "Route updated · 4 min faster", Snackbar.LENGTH_LONG)
    .setAction("Undo") { undo() }   // omit the action while driving
    .show()
