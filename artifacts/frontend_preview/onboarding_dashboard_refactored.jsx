
// Sidebar Component
function Sidebar() {
  const menuItems = [
    { icon: "🏠", label: "Dashboard" },
    { icon: "👤", label: "Profile" },
    { icon: "📝", label: "Tasks" },
    { icon: "📅", label: "Calendar" },
    { icon: "❓", label: "Support" },
  ];

  return (
    <div className="flex flex-col bg-teal-600 h-full w-64 p-6 rounded-tr-lg">
      <div className="text-white font-bold text-lg pb-6">Ascend</div>
      <div className="space-y-4">
        {menuItems.map((item) => (
          <div
            key={item.label}
            className="flex items-center text-white py-2 px-3 rounded hover:bg-teal-700 cursor-pointer"
          >
            <span className="mr-2">{item.icon}</span>
            {item.label}
          </div>
        ))}
      </div>
    </div>
  );
}

// Header Component
function Header() {
  return (
    <div className="flex justify-between items-center bg-navy-900 p-4 rounded-lg mb-8">
      <div className="text-white font-bold">Onboarding Platform</div>
      <div className="relative">
        <button className="bg-gray-300 rounded-full h-10 w-10 flex items-center justify-center">
          JD
        </button>
        {/* Dropdown Placeholder */}
      </div>
    </div>
  );
}

// WelcomeMessage Component
function WelcomeMessage() {
  return (
    <div className="text-center mb-8">
      <h1 className="text-2xl font-bold mb-4">
        Welcome to Ascend, Jane Doe!
      </h1>
      <button className="bg-teal-600 text-white py-3 px-6 rounded hover:bg-teal-700">
        Start Your Journey
      </button>
    </div>
  );
}

// Card Component
function Card({ title, children }) {
  return (
    <div className="bg-white shadow p-6 rounded flex-1">
      <h2 className="font-bold mb-4">{title}</h2>
      {children}
    </div>
  );
}

// UserProgress Component
function UserProgress() {
  return (
    <Card title="User Progress">
      <div className="flex items-center space-x-4">
        <div className="w-16 h-16 rounded-full border-4 border-teal-600 flex items-center justify-center">
          60%
        </div>
        <div>
          <p>60% Complete</p>
          <p>3/5 Modules done.</p>
          <p>Next: Compliance Training</p>
        </div>
      </div>
    </Card>
  );
}

// InputForms Component
function InputForms() {
  const forms = ["Complete W-4 Tax Form", "Sign Company Handbook"];

  return (
    <Card title="Input Forms">
      <ul className="space-y-2">
        {forms.map((form) => (
          <li
            key={form}
            className="bg-gray-100 hover:bg-gray-200 p-3 rounded cursor-pointer"
          >
            {form}
          </li>
        ))}
      </ul>
    </Card>
  );
}

// QuickTips Component
function QuickTips() {
  const resources = ["Security Guide", "IT Setup Checklist"];

  return (
    <Card title="Quick Tips">
      <p className="mb-4">💡 Set up your direct deposit early!</p>
      <h3 className="font-bold mb-2">Resource Library</h3>
      <ul className="space-y-2">
        {resources.map((resource) => (
          <li
            key={resource}
            className="bg-gray-100 hover:bg-gray-200 p-3 rounded cursor-pointer flex items-center justify-between"
          >
            {resource}
          </li>
        ))}
      </ul>
    </Card>
  );
}

// Dashboard Component
function Dashboard() {
  return (
    <div className="h-screen flex bg-gray-100">
      <Sidebar />
      <div className="flex-1 p-8">
        <Header />
        <WelcomeMessage />
        <div className="flex justify-between space-x-4">
          <UserProgress />
          <InputForms />
          <QuickTips />
        </div>
      </div>
    </div>
  );
}

// Render the component into the root element using React 18 API (UMD global ReactDOM)
const rootElement = document.getElementById('root');
if (rootElement) {
  const root = ReactDOM.createRoot(rootElement);
  root.render(<Dashboard />);
}

// No ES module export needed for in-browser preview