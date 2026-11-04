// Views: PopupMenu with the overlay
val popup = PopupMenu(ContextThemeWrapper(this, R.style.ThemeOverlay_Ivi_PopupMenu), anchor)
popup.menuInflater.inflate(R.menu.route_options, popup.menu)
popup.show()
