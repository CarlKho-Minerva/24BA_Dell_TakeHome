const typeLabels = {
  missing_from_ecb: "Missing from ECB",
  missing_from_tar: "Missing from TAR",
  charge_mismatch: "Charge Mismatch",
  stop_date_mismatch: "Stop Date Mismatch",
  new_charge_mismatch: "New Charge Mismatch",
};

const systemCodes = {
  VP001: "VP001",
  VP068: "VP068",
  VP227: "VP227",
  VP324: "VP324",
};

const DEV_MODE = true; // Set to false in production
const DEFAULT_FILES = {
  tar: "/Users/cvk/Downloads/[CODE] Local Projects/Dell_TakeHome/ServiceCodes_TAR.csv",
  ecb: "/Users/cvk/Downloads/[CODE] Local Projects/Dell_TakeHome/ServiceCodes_ECB.csv",
};

function loadSavedFilePaths() {
  if (DEV_MODE) {
    return DEFAULT_FILES;
  }
  const saved = JSON.parse(sessionStorage.getItem("lastUsedFiles") || "{}");
  return saved;
}

document.getElementById("upload-form").onsubmit = async (e) => {
  e.preventDefault();
  showLoading(true);

  try {
    const formData = new FormData(e.target);

    // In DEV_MODE, if files are not selected, use default files on the server
    if (DEV_MODE) {
      const tarFile = formData.get("tar_file");
      const ecbFile = formData.get("ecb_file");

      if (!tarFile.name) {
        formData.delete("tar_file");
        formData.append("tar_file_path", DEFAULT_FILES.tar);
      }
      if (!ecbFile.name) {
        formData.delete("ecb_file");
        formData.append("ecb_file_path", DEFAULT_FILES.ecb);
      }
    }

    const response = await fetch("/compare", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    if (response.ok) {
      // Store total records from the response
      window.totalRecordsFromResponse = data.total_records;

      // Store the original discrepancies for filtering
      window.originalDiscrepancies = data.discrepancies;

      displayResults(data.discrepancies);
      showToast("Success", "Files compared successfully!", "success");
    } else {
      throw new Error(data.error || "Failed to compare files");
    }
  } catch (error) {
    showToast("Error", error.message, "error");
    clearResults();
  } finally {
    showLoading(false);
  }
};

function displayResults(discrepancies) {
  const accordion = document.getElementById("discrepancyAccordion");
  accordion.innerHTML = "";

  // Ensure all discrepancy types are shown
  const allTypes = Object.keys(typeLabels);
  const grouped = allTypes.reduce((acc, type) => {
    acc[type] = discrepancies.filter((d) => d.type === type);
    return acc;
  }, {});

  displaySummary(grouped);

  // Create accordion items for all types
  Object.entries(typeLabels).forEach(([type, label], index) => {
    const items = grouped[type] || [];
    const accordionItem = createAccordionItem(type, items, label, index);
    accordion.appendChild(accordionItem);
  });
}

function createAccordionItem(type, items, label, index) {
  const div = document.createElement("div");
  div.className = "accordion-item";

  const content =
    items.length > 0
      ? items.map((item) => createDiscrepancyItem(item)).join("")
      : `<div class="empty-state">
         <i class="bi bi-check-circle"></i>
         <p>No ${label.toLowerCase()} discrepancies found</p>
       </div>`;

  div.innerHTML = `
    <h2 class="accordion-header">
        <button class="accordion-button ${
          index > 0 ? "collapsed" : ""
        }" type="button"
                data-bs-toggle="collapse" data-bs-target="#collapse${index}">
            ${label}
            <span class="badge bg-secondary ms-2">${items.length}</span>
        </button>
    </h2>
    <div id="collapse${index}" class="accordion-collapse collapse ${
    index === 0 ? "show" : ""
  }"
         data-bs-parent="#discrepancyAccordion">
        <div class="accordion-body">
            ${content}
        </div>
    </div>
`;
  return div;
}

function createDiscrepancyItem(item) {
  const codeInfo = systemCodes[item.service_code] || "Service Code";

  // Insert a space between service_code and spa
  const formattedServiceCode = formatCode(item.service_code);

  return `
        <div class="discrepancy-item">
            <span class="system-code code-tooltip" title="${codeInfo}">${formattedServiceCode}</span>
            <span class="type-badge">${item.spa}</span>
            ${createComparisonView(item)}
        </div>
    `;
}

function formatCode(code) {
  // Insert space between parts of the code, e.g., 'VP00181557000TOT' to 'VP001 81557000TOT'
  // Adjust the logic based on your actual code patterns
  return code.replace(/([A-Z]+)(\d+)/, "$1 $2");
}

// Initialize tooltips after content is added
document.addEventListener("DOMContentLoaded", () => {
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll("[title]")
  );
  tooltipTriggerList.map((el) => new bootstrap.Tooltip(el));

  // Restore last used files
  const savedFiles = loadSavedFilePaths();
  if (savedFiles.tar) {
    document
      .getElementById("tar-file")
      .setAttribute("data-default", savedFiles.tar);
  }
  if (savedFiles.ecb) {
    document
      .getElementById("ecb-file")
      .setAttribute("data-default", savedFiles.ecb);
  }

  renderFilterOptions();
});

// Add visual feedback for file validation
document.querySelectorAll('input[type="file"]').forEach((input) => {
  input.addEventListener("change", (e) => {
    const file = e.target.files[0];
    const feedback = document.createElement("div");

    if (file && file.name.endsWith(".csv")) {
      feedback.className = "valid-feedback d-block";
      feedback.textContent = `File selected: ${file.name}`;
    } else {
      feedback.className = "invalid-feedback d-block";
      feedback.textContent = "Please select a CSV file";
    }

    const existing = input.parentNode.querySelector(
      ".valid-feedback, .invalid-feedback"
    );
    if (existing) existing.remove();
    input.parentNode.appendChild(feedback);
  });
});

function showLoading(show) {
  const spinner = document.getElementById("loading-spinner");
  const submitBtn = document.getElementById("submit-btn");
  spinner.classList.toggle("d-none", !show);
  submitBtn.disabled = show;
}

function showToast(title, message, type) {
  const toast = document.getElementById("statusToast");
  const toastTitle = document.getElementById("toastTitle");
  const toastMessage = document.getElementById("toastMessage");

  toastTitle.textContent = title;
  toastMessage.textContent = message;
  toast.classList.toggle("bg-danger", type === "error");
  toast.classList.toggle("bg-success", type === "success");

  const bsToast = new bootstrap.Toast(toast);
  bsToast.show();
}

function displaySummary(grouped) {
  const summary = document.getElementById("summary");
  const totalDiscrepancies = Object.values(grouped).flat().length;
  const totalRecords = getTotalRecords(); // Implement this function
  const discrepancyPercentage = totalRecords
    ? ((totalDiscrepancies / totalRecords) * 100).toFixed(2)
    : 0;

  const summaryHtml = `
        <h4>Summary of Discrepancies</h4>
        <ul class="list-unstyled">
            ${Object.entries(grouped)
              .map(
                ([type, items]) => `
                <li class="mb-1">
                    <strong>${typeLabels[type]}:</strong> ${items.length} issues
                </li>
            `
              )
              .join("")}
            <li class="mt-2">
                <strong>Total Discrepancies:</strong> ${totalDiscrepancies} / ${totalRecords} records (${discrepancyPercentage}%)
            </li>
        </ul>
    `;

  summary.innerHTML = summaryHtml;
  summary.classList.remove("d-none");
}

function getTotalRecords() {
  // Use the totalRecordsFromResponse set in the onsubmit function
  return window.totalRecordsFromResponse || 0;
}

function createComparisonView(item) {
  if (item.type.includes("missing_from")) {
    return `<div class="alert alert-warning">
        ${
          item.type === "missing_from_ecb"
            ? "Record exists in TAR but not in ECB"
            : "Record exists in ECB but not in TAR"
        }
    </div>`;
  }

  return `
    <div class="comparison-grid">
        <div class="value-box tar-value">
            <small class="text-muted">TAR Value</small>
            <div class="mt-1"><strong>${item.tar_value || "N/A"}</strong></div>
        </div>
        <div class="value-box ecb-value">
            <small class="text-muted">ECB Value</small>
            <div class="mt-1"><strong>${item.ecb_value || "N/A"}</strong></div>
        </div>
    </div>
`;
}

function clearResults() {
  const resultsDiv = document.getElementById("results");
  const accordion = document.getElementById("discrepancyAccordion");
  const summary = document.getElementById("summary");

  accordion.innerHTML = "";
  summary.classList.add("d-none");
  summary.innerHTML = "";
}

function renderFilterOptions() {
  const filterPanel = document.querySelector(".filter-options");
  filterPanel.innerHTML = "";

  Object.entries(systemCodes).forEach(([code, description]) => {
    const label = document.createElement("label");
    label.innerHTML = `
            <input type="checkbox" value="${code}" checked>
            ${description}
        `;
    filterPanel.appendChild(label);
  });

  // Add event listener for filter changes
  document
    .querySelectorAll('.filter-options input[type="checkbox"]')
    .forEach((checkbox) => {
      checkbox.addEventListener("change", () => {
        applyFilters();
      });
    });
}

function applyFilters() {
  const selectedCodes = Array.from(
    document.querySelectorAll('.filter-options input[type="checkbox"]:checked')
  ).map((cb) => cb.value);

  const filteredDiscrepancies = window.originalDiscrepancies.filter(
    (discrepancy) => {
      // Exclude TOT and SYS codes
      if (
        discrepancy.service_code.includes("TOT") ||
        discrepancy.service_code.includes("SYS")
      ) {
        return false;
      }
      return selectedCodes.includes(discrepancy.service_code);
    }
  );

  displayResults(filteredDiscrepancies);
}

// Initialize on document load
document.addEventListener("DOMContentLoaded", () => {
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll("[title]")
  );
  tooltipTriggerList.map((el) => new bootstrap.Tooltip(el));

  const savedFiles = loadSavedFilePaths();
  if (savedFiles.tar) {
    document
      .getElementById("tar-file")
      .setAttribute("data-default", savedFiles.tar);
  }
  if (savedFiles.ecb) {
    document
      .getElementById("ecb-file")
      .setAttribute("data-default", savedFiles.ecb);
  }

  renderFilterOptions();
});