const BASE_URL = "http://localhost:8000";

document.addEventListener("DOMContentLoaded", () => {
  loadStudents();
  loadUniversities();
  setupForms();
});

function setupForms() {
  document.getElementById("studentForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = document.getElementById("studentName").value.trim();
    if (!name) return;

    try {
      const response = await fetch(`${BASE_URL}/students`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name }),
      });

      if (!response.ok) throw new Error("Failed to add student");
      document.getElementById("studentName").value = "";
      await loadStudents();
    } catch (error) {
      alert("Error adding student.");
      console.error(error);
    }
  });

  document.getElementById("linkForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const studentId = document.getElementById("studentSelect").value;
    const universityId = document.getElementById("universitySelect").value;

    if (!studentId || !universityId) return;

    try {
      const response = await fetch(`${BASE_URL}/link`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          student_id: parseInt(studentId),
          university_id: parseInt(universityId)
        }),
      });

      if (!response.ok) throw new Error("Failed to link student");
      await loadStudents();
    } catch (error) {
      alert("Error linking student.");
      console.error(error);
    }
  });
}

async function loadStudents() {
  try {
    const response = await fetch(`${BASE_URL}/students`);
    const students = await response.json();

    console.log("📥 Loaded students:", students); // DEBUG

    const tableBody = document.querySelector("#studentTable tbody");
    const studentSelect = document.getElementById("studentSelect");
    tableBody.innerHTML = "";
    studentSelect.innerHTML = `<option value="">Select Student</option>`;

    students.forEach((student) => {
      const row = tableBody.insertRow();
      row.insertCell().textContent = student.id;
      row.insertCell().textContent = student.name;
      row.insertCell().textContent = student.university_name || "Not linked";

      const option = document.createElement("option");
      option.value = student.id;
      option.textContent = student.name;
      studentSelect.appendChild(option);
    });
  } catch (error) {
    alert("Error loading students.");
    console.error(error);
  }
}

async function loadUniversities() {
  try {
    const response = await fetch(`${BASE_URL}/universities`);
    const universities = await response.json();

    console.log("📚 Loaded universities:", universities); // DEBUG

    const universitySelect = document.getElementById("universitySelect");
    universitySelect.innerHTML = `<option value="">Select University</option>`;

    universities.forEach((uni) => {
      const option = document.createElement("option");
      option.value = uni.id;
      option.textContent = uni.name;
      universitySelect.appendChild(option);
    });
  } catch (error) {
    alert("Error loading universities.");
    console.error(error);
  }
}
