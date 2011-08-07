var statusWindow = null;

function OpenStatusWindow() {
	if (statusWindow==null || !statusWindow.isActive()) {
		statusWindow = Titanium.UI.createWindow({
			id: "statusWindow",
			url: "app://statusWindow.html"
		});
		statusWindow.open();
	} else {
		statusWindow.focus();
	}
}