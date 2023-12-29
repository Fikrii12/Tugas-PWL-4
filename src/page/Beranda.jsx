import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import axios from "axios";

function Beranda() {
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    movieName: "",
    image: null,
  });
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetchMovies();
  }, []);

  const fetchMovies = async () => {
    try {
      const response = await axios.get('/api/get_movies');
      setMovies(response.data.movies);
    } catch (error) {
      console.error('Error fetching movies:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setFormData((prevData) => ({
      ...prevData,
      image: file,
    }));
  };

  const handleAddData = async (e) => {
    e.preventDefault();

    const form = new FormData();
    form.append('movieName', formData.movieName);
    form.append('image', formData.image);

    try {
      const response = await axios.post('/api/save_movie', form);
      console.log(response.data);

      setFormData({
        movieName: "",
        image: null,
      });

      setShowModal(false);

      // Setelah menambahkan film, perbarui daftar film
      fetchMovies();
    } catch (error) {
      console.error('Error saving movie:', error);
    }
  };

  const handleDeleteMovie = async (movieName) => {
    try {
      const response = await fetch(`/api/delete_movie/${movieName}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        // Refresh daftar film setelah penghapusan berhasil
        fetchMovies();
        alert('Movie deleted successfully');
      } else {
        const errorData = await response.json();
        alert(errorData.message || 'Failed to delete movie');
      }
    } catch (error) {
      console.error('There was an error:', error);
      alert('An error occurred while deleting the movie');
    }
  };

  return (
    <div>
      <Navbar className={`bg-body-tertiary`} expand="lg">
        <Container>
          <Navbar.Brand className="nav-text" href="/">
            Budi Movie
          </Navbar.Brand>
          <Navbar.Toggle aria-controls="responsive-navbar-nav" />
          <Navbar.Collapse id="responsive-navbar-nav">
            <Nav className="ms-auto">
              <Button
                variant="primary"
                className="me-3"
                onClick={() => setShowModal(true)}
              >
                Tambah Data
              </Button>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* Modal */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Tambah Data Film</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleAddData}>
            <Form.Group controlId="movieName">
              <Form.Label>Nama Film</Form.Label>
              <Form.Control
                type="text"
                placeholder="Masukkan nama film"
                name="movieName"
                value={formData.movieName}
                onChange={handleInputChange}
              />
            </Form.Group>
            <Form.Group controlId="image">
              <Form.Label>Gambar Film</Form.Label>
              <Form.Control
                type="file"
                accept="image/*"
                onChange={handleImageChange}
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Tambah Data
            </Button>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Batal
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Tampilkan daftar film */}
      <Container>
        <h2>List of Movies</h2>
        <ul>
          {movies.map((movie, index) => (
            <li key={index}>
              <p>{movie.movieName}</p>
              <img src={movie.image} alt={movie.movieName} style={{ width: '150px', height: '200px' }} />
              <button onClick={() => handleDeleteMovie(movie.movieName)}>Delete</button>
            </li>
          ))}
        </ul>
      </Container>
    </div>
  );
}

export default Beranda;
