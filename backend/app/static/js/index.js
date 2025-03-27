let currentLanguage = "en";
let questionsData = {};
let feedbackData = {};
let currentSectionIndex = 0;
let sections = {};

const options = {
  en: ["Strongly Disagree", "Disagree", "Somewhat Agree", "Agree", "Strongly Agree"],
  ar: ["أعارض بشدة", "أعارض", "أوافق جزئيًا", "أوافق", "أوافق بشدة"],
};

// Load JSON files (questions & feedback)
$(document).ready(function () {
  fetch("static/data/zWPa15oNvBxkEfulAqRQZOL.json")
    .then((response) => response.json())
    .then((data) => {
      questionsData = data;
      sections = {
        en: Object.keys(data),
        ar: Object.keys(data).map((key) => data[key].ar_pillar_name),
      };

      if (document.getElementById("questionnaire")) {
        loadSection();
      }
    })
    .catch((error) => console.error("Error loading questions:", error));

  fetch("feedback.json")
    .then((response) => response.json())
    .then((data) => {
      feedbackData = data;
      if (document.getElementById("feedbackContent")) {
        loadFeedbackPage();
      }
    })
    .catch((error) => console.error("Error loading feedback:", error));
});

// Load the Current Section for Questions Page
function loadSection() {
  const sectionKey = sections.en[currentSectionIndex];
  const sectionName = questionsData[sectionKey][`${currentLanguage}_pillar_name`];
  const questions = questionsData[sectionKey].questions || [];

  let html = `<h3 class="text-center">${currentLanguage === "en" ? "Pillar:" : "الركيزة:"} ${sectionName}</h3>`;

  if (questions.length === 0) {
    console.error(`No questions found for: ${sectionKey}`, questionsData);
    html += `<p style="color:red;">⚠ No questions available for this section.</p>`;
  }

  let storedData = JSON.parse(localStorage.getItem("allResponses")) || {};
  let answers = storedData[sectionKey] || {};

  questions.forEach((q, index) => {
    const storedValue = answers[index] || "";

    html += `
        <div class="question-card">
            <p class="question">${q[currentLanguage]}</p>
            <div class="options-group">
    `;

    options[currentLanguage].forEach((option, i) => {
      const isChecked = storedValue === i.toString() ? "checked" : "";
      html += `
        <div class="form-check">
          <input class="form-check-input" type="radio" name="q${index}" id="q${index}_${i}" value="${i}" ${isChecked}
                onchange="saveResponse('${sectionKey}', ${index}, this.value)">
          <label class="form-check-label" for="q${index}_${i}">
            ${option}
          </label>
        </div>
      `;
    });

    html += `</div></div>`;
  });

  if (currentSectionIndex === sections.en.length - 1) {
    html += `<div class="btn-container mt-4">
              <button class="btn btn-primary" onclick="calculateAndSubmit()">Submit All Answers</button>
             </div>`;
  }

  $("#questionnaire").html(html);
  updateButtons();
  scrollToTop();
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Save Response
function saveResponse(section, index, value) {
  let storedData = JSON.parse(localStorage.getItem("allResponses")) || {};

  if (!storedData[section]) {
    storedData[section] = {};
  }

  storedData[section][index] = value;
  localStorage.setItem("allResponses", JSON.stringify(storedData));
}

// Validate Before Navigating
function validateSection() {
  const sectionKey = sections.en[currentSectionIndex];
  const questions = questionsData[sectionKey] || [];

  let storedData = JSON.parse(localStorage.getItem("allResponses")) || {};
  let answers = storedData[sectionKey] || {};

  if (Object.keys(answers).length < questions.length) {
    alert(currentLanguage === "en" ? "Please answer all questions before moving to the next section." : "يرجى الإجابة على جميع الأسئلة قبل الانتقال إلى القسم التالي.");
    return false;
  }
  return true;
}

// Navigate to Previous Section
function prevSection() {
  if (currentSectionIndex > 0) {
    if (!validateSection()) return;
    currentSectionIndex--;
    loadSection();
  }
}

// Navigate to Next Section
function nextSection() {
  if (currentSectionIndex < sections.en.length - 1) {
    if (!validateSection()) return;
    currentSectionIndex++;
    loadSection();
  }
}

// Update Navigation Buttons
function updateButtons() {
  $("#prevButton").toggle(currentSectionIndex > 0);
  $("#nextButton").toggle(currentSectionIndex < sections.en.length - 1);
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

// Load Feedback Page
function loadFeedbackPage() {
  let results = JSON.parse(localStorage.getItem("feedbackResults")) || {};

  if (!Object.keys(results).length) {
    console.error("No feedback results found in localStorage.");
    return;
  }

  let progressBarsHTML = "";
  let feedbackHTML = "";
  let tableHTML = "";

  Object.keys(results).forEach((pillar) => {
    let data = results[pillar];
    let percentage = (data.averageScore / 5) * 100;
    let translatedPillar = questionsData[pillar][`${currentLanguage}_pillar_name`];
    let scoreKey = data.averageScore.toString();
    let feedbackText = feedbackData[pillar] && feedbackData[pillar].feedback[scoreKey] ? feedbackData[pillar].feedback[scoreKey][currentLanguage] : "Feedback not available.";

    progressBarsHTML += `
        <div class="progress-item">
            <label>${translatedPillar}</label>
            <div class="progress">
                <div class="progress-bar" style="width: ${percentage}%;"></div>
            </div>
        </div>
    `;

    feedbackHTML += `
        <div class="mt-3">
            <h5>${translatedPillar}</h5>
            <p>${feedbackText}</p>
        </div>
    `;

    tableHTML += `
        <tr>
            <td>${translatedPillar}</td>
            <td>${data.averageScore}</td>
            <td>${data.averageScore >= 4 ? "Low" : data.averageScore === 3 ? "Medium" : "High"}</td>
        </tr>
    `;
  });

  document.getElementById("progressBars").innerHTML = `<div class="row">${progressBarsHTML}</div>`;
  document.getElementById("feedbackContent").innerHTML = feedbackHTML;
  document.getElementById("progressTable").innerHTML = tableHTML;
}

// Calculate Scores & Generate Feedback Page
function calculateAndSubmit() {
  let results = {};
  let storedData = JSON.parse(localStorage.getItem("allResponses")) || {};

  sections.en.forEach((section, index) => {
    const questions = questionsData[section].questions || [];
    let total = 0;
    let count = 0;

    if (storedData[section]) {
      Object.values(storedData[section]).forEach((val) => {
        total += parseInt(val) + 1;
        count++;
      });
    }

    const averageScore = count > 0 ? Math.round(total / count) : 0;
    results[section] = {
      averageScore: averageScore,
    };
  });

  localStorage.setItem("feedbackResults", JSON.stringify(results));
  setTimeout(() => {
    window.location.href = "/feedback";
  }, 300);
}
