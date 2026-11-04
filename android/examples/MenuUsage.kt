// Views: PopupMenu with the Aurora overlay
val popup = PopupMenu(ContextThemeWrapper(this, R.style.ThemeOverlay_Aurora_PopupMenu), anchor)
popup.menuInflater.inflate(R.menu.route_options, popup.menu)
popup.show()
