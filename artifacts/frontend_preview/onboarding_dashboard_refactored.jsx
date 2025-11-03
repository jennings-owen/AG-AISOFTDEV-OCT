function Sidebar() {
  return (
    <aside className="flex flex-col bg-blue-900 text-white w-1/4 p-4">
      <h1 className="text-2xl mb-8">Ascend Onboarding Platform</h1>
      <nav>
        <ul>
          {["Dashboard", "Learning Path", "Resources", "Profile"].map((item) => (
            <li key={item} className="text-lg py-2 px-4 hover:bg-teal-500">{item}</li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}

function Header({ username }) {
  return (
    <header className="flex justify-between items-center mb-8">
      <h2 className="text-3xl font-bold">Welcome, {username}!</h2>
      <div className="rounded-full bg-gray-300 w-10 h-10" />
    </header>
  );
}

function WelcomeSection() {
  return (
    <section className="text-center mb-8">
      <p className="text-lg">Let's get started on your journey with Ascend.</p>
      <button className="mt-4 px-6 py-2 bg-teal-500 text-white rounded shadow hover:bg-teal-600">
        Start Your Onboarding
      </button>
    </section>
  );
}

function ProgressTracker() {
  return (
    <div className="bg-white rounded shadow p-4 flex flex-col items-center">
      <h3 className="font-semibold mb-2">User Progress Tracker</h3>
      <div className="text-teal-500 text-2xl">60%</div>
      <p>Onboarding Progress: 60% Complete</p>
    </div>
  );
}

function InputForms() {
  return (
    <div className="bg-white rounded shadow p-4">
      <h3 className="font-semibold mb-4">Input Forms</h3>
      {["Personal Information", "Emergency Contact"].map((form) => (
        <button key={form} className="flex justify-between items-center w-full p-2 mb-2 bg-teal-100 hover:bg-teal-200 rounded">
          {form}
        </button>
      ))}
    </div>
  );
}

function TipsAndResources() {
  return (
    <div className="bg-white rounded shadow p-4">
      <h3 className="font-semibold mb-4">Tips and Resources</h3>
      <input type="text" placeholder="Search resources..." className="border rounded p-2 w-full mb-4" />
      <div className="flex gap-4">
        {["Policies", "Tools"].map((resource) => (
          <div key={resource} className="flex-1 p-2 bg-gray-100 rounded text-center">{resource}</div>
        ))}
      </div>
    </div>
  );
}

function MentorInfo() {
  return (
    <div className="bg-white rounded shadow p-4 flex items-center">
      <img src="#" alt="Mentor" className="w-12 h-12 rounded-full mr-4" />
      <div>
        <h4 className="font-semibold">Jane Doe - Your Mentor</h4>
        <p>Contact: jane.doe@ascend.com</p>
        <p>Suggested Topic: Team Introductions</p>
      </div>
    </div>
  );
}

function Dashboard() {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <main className="flex-1 p-8 bg-gray-100">
        <Header username="Sarah" />
        <WelcomeSection />
        <div className="grid grid-cols-2 gap-8">
          <ProgressTracker />
          <InputForms />
          <TipsAndResources />
          <MentorInfo />
        </div>
      </main>
    </div>
  );
}

// Render the component into the root element using React 18 API (UMD global ReactDOM)
const rootElement = document.getElementById('root');
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(<Dashboard />);
}