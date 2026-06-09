
import {useAuth} from "@/core/auth/AuthProvider";
export default function A() {
  const { user, isAuthenticated } = useAuth();

  return (
    <div>
      <h1>Welcome!</h1>
      {isAuthenticated ? (
        <p>Hello, {user?.name}! <a href="/workspace">Go to Dashboard</a></p>
      ) : (
        <p><a href="/login">Please login</a> to continue</p>
      )}
    </div>
  );
}
