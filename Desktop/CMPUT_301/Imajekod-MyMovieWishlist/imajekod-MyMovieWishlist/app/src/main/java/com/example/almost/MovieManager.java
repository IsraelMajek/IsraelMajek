package com.example.almost;

import android.content.Context;
import android.content.DialogInterface;
import android.view.View;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Toast;
import androidx.appcompat.app.AlertDialog;
import java.util.ArrayList;

public class MovieManager {

    private Context context;
    private ArrayList<MovieData> movieCollection;
    private MovieAdapter movieAdapter;
    private MainActivity mainActivity;

    public MovieManager(MainActivity activity, ArrayList<MovieData> movieCollection, MovieAdapter adapter) {
        this.context = activity;
        this.movieCollection = movieCollection;
        this.movieAdapter = adapter;
        this.mainActivity = activity;
    }

    public void openMovieDialog(MovieData movie, int index) {
        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        builder.setTitle(movie == null ? "Add a Movie" : "Edit Movie");

        View dialogView = View.inflate(context, R.layout.adding_movies, null);
        builder.setView(dialogView);

        final EditText titleInput = dialogView.findViewById(R.id.edit_text_movie_text);
        final EditText directorInput = dialogView.findViewById(R.id.edit_text_director_text);
        final EditText genreInput = dialogView.findViewById(R.id.edit_text_genre_text);
        final EditText yearInput = dialogView.findViewById(R.id.edit_text_year_text);
        CheckBox watchedCheckBox = dialogView.findViewById(R.id.have_watched);

        if (movie != null) {
            titleInput.setText(movie.getTitle());
            directorInput.setText(movie.getDirector());
            genreInput.setText(movie.getGenre());
            yearInput.setText(movie.getYear());
            watchedCheckBox.setChecked(movie.isWatched());
        }

        builder.setPositiveButton("Save", (dialog, which) -> {
            String title = titleInput.getText().toString();
            String director = directorInput.getText().toString();
            String genre = genreInput.getText().toString();
            String year = yearInput.getText().toString();
            boolean watched = watchedCheckBox.isChecked();

            if (title.isEmpty() || director.isEmpty() || genre.isEmpty() || year.isEmpty() || year.length() != 4) {
                Toast.makeText(context, "Fill in all fields correctly.", Toast.LENGTH_SHORT).show();
                return;
            }

            if (movie == null) {
                movieCollection.add(new MovieData(title, director, genre, year, watched));

                mainActivity.totalMovies++;
                if (watched) mainActivity.watchedMovies++;
            } else {
                if (watched && !movie.isWatched()) mainActivity.watchedMovies++;
                else if (!watched && movie.isWatched()) mainActivity.watchedMovies--;

                movie.setTitle(title);
                movie.setDirector(director);
                movie.setGenre(genre);
                movie.setYear(year);
                movie.setWatched(watched);
            }

            movieAdapter.notifyDataSetChanged();
            mainActivity.updateMovieStats();

        });

        builder.setNegativeButton("Cancel", (dialog, which) -> dialog.dismiss());
        builder.show();
    }
}
