// Views: MaterialAlertDialogBuilder with the overlay
MaterialAlertDialogBuilder(this, R.style.ThemeOverlay_Ivi_Dialog)
    .setIcon(R.drawable.ic_phone)
    .setTitle("Forget Pixel 9?")
    .setMessage("You will need to pair again.")
    .setNegativeButton("Cancel", null)
    .setPositiveButton("Forget") { _, _ -> forget() }
    .show()
