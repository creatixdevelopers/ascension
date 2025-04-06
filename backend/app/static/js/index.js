let currentLanguage = "en";

function scrollToTop() {
	window.scrollTo({top: 0, behavior: "smooth"});
}

function toggleLanguage() {
	currentLanguage = document.getElementById("languageToggle").checked ? "ar" : "en";

	let questionSection = document.getElementById("questions");
	if (questionSection) {
		questionSection.classList.toggle("rtl", currentLanguage === "ar");
		document.documentElement.setAttribute("dir", currentLanguage === "ar" ? "rtl" : "ltr");
	}

	let feedbackSection = document.querySelector(".feedback-section");
	if (feedbackSection) {
		feedbackSection.classList.toggle("rtl", currentLanguage === "ar");
	}

	if (document.getElementById("questionnaire")) {
		loadSection();
	}

	if (document.getElementById("feedbackContent")) {
		loadFeedbackPage();
	}
}
