import { useState } from "react";
import { Link } from "react-router-dom";
import "./Profile.css";

function Profile() {
  // Mock initial data - in a real app, this would come from an API/Context
  const [profile, setProfile] = useState({
    username: "coolUser123",
    email: "user@example.com",
    displayName: "Cool User",
    bio: "I love hiking and coding! Looking for friends.",
    age: 25,
    gender: "Non-binary",
    interests: "Hiking, Coding, Movies, Coffee",
    avatarUrl: "https://via.placeholder.com/150",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProfile((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Saving profile:", profile);
    // TODO: Call API to update profile
    alert("Profile updated successfully!");
  };

  return (
    <div className="profile-container">
      <Link to="/" className="back-link">
        &larr; Back to Home
      </Link>
      <div className="profile-header">
        <img src={profile.avatarUrl} alt="Profile" className="profile-avatar" />
        <div className="profile-info">
          <h2>{profile.displayName || profile.username}</h2>
          <p>@{profile.username}</p>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="profile-section">
          <h3>Basic Information</h3>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="displayName">Display Name</label>
              <input
                type="text"
                id="displayName"
                name="displayName"
                value={profile.displayName}
                onChange={handleChange}
              />
            </div>
            <div className="form-group">
              <label htmlFor="age">Age</label>
              <input
                type="number"
                id="age"
                name="age"
                value={profile.age}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="gender">Gender</label>
              <select
                id="gender"
                name="gender"
                value={profile.gender}
                onChange={handleChange}
              >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Non-binary">Non-binary</option>
                <option value="Other">Other</option>
                <option value="Prefer not to say">Prefer not to say</option>
              </select>
            </div>
            <div className="form-group">
              <label htmlFor="email">Email (Read Only)</label>
              <input
                type="email"
                id="email"
                value={profile.email}
                disabled
                style={{ opacity: 0.7, cursor: "not-allowed" }}
              />
            </div>
          </div>
        </div>

        <div className="profile-section">
          <h3>About Me</h3>
          <div className="form-group">
            <label htmlFor="bio">Bio</label>
            <textarea
              id="bio"
              name="bio"
              value={profile.bio}
              onChange={handleChange}
              placeholder="Tell us about yourself..."
            />
          </div>
          <div className="form-group">
            <label htmlFor="interests">Interests (comma separated)</label>
            <input
              type="text"
              id="interests"
              name="interests"
              value={profile.interests}
              onChange={handleChange}
              placeholder="e.g. Music, Travel, Reading"
            />
          </div>
        </div>

        <div className="profile-section">
          <h3>Photo Wall</h3>
          <div className="photo-wall">
            {/* Mock photos */}
            <div
              className="photo-placeholder"
              style={{
                backgroundImage: "url(https://via.placeholder.com/100)",
              }}
            ></div>
            <div
              className="photo-placeholder"
              style={{
                backgroundImage: "url(https://via.placeholder.com/100)",
              }}
            ></div>
            <div className="photo-placeholder">+ Add Photo</div>
          </div>
        </div>

        <button type="submit" className="save-button">
          Save Changes
        </button>
      </form>
    </div>
  );
}

export default Profile;
