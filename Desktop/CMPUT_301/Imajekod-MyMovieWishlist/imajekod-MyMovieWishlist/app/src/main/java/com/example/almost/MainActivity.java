package com.example.almost;

import android.content.DialogInterface;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {

    private TextView totalMoviesView;
    public int totalMovies = 0;
    public int watchedMovies = 0;
    private TextView watchedMoviesView;
    private ArrayList<MovieData> movieCollection;
    private ListView movieListView;
    private MovieAdapter movieAdapter;
    private MovieManager movieManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        totalMoviesView = findViewById(R.id.my_movies);
        watchedMoviesView = findViewById(R.id.movies_watched);

        movieCollection = new ArrayList<>();
        movieListView = findViewById(R.id.movie_list);
        movieAdapter = new MovieAdapter(this, movieCollection);
        movieListView.setAdapter(movieAdapter);

        movieManager = new MovieManager(this, movieCollection, movieAdapter);

        movieListView.setOnItemClickListener((parent, view, position, id) -> showOptionsDialog(position));

        findViewById(R.id.add_movie).setOnClickListener(view -> movieManager.openMovieDialog(null, -1));
    }

    private void showOptionsDialog(int position) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Select an Action");

        String[] options = {"Edit", "Delete"};

        builder.setItems(options, (dialog, choice) -> {
            if (choice == 0) {
                movieManager.openMovieDialog(movieCollection.get(position), position);
            } else {
                removeMovie(position);
            }
        });

        builder.show();
    }

    private void removeMovie(int index) {
        MovieData removedMovie = movieCollection.get(index);

        if (removedMovie.isWatched()) watchedMovies--;
        totalMovies--;

        movieCollection.remove(index);
        movieAdapter.notifyDataSetChanged();
        updateMovieStats();
    }

    public void updateMovieStats() {
        totalMoviesView.setText("Movies: " + totalMovies);
        watchedMoviesView.setText("Watched: " + watchedMovies);
    }
}
