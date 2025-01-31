package com.example.almost;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

import com.example.almost.MovieData;

import java.util.ArrayList;

public class MovieAdapter extends ArrayAdapter<MovieData> {

    public MovieAdapter(Context context, ArrayList<MovieData> movies) {
        super(context, 0, movies);
    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent) {
        if (convertView == null) {
            convertView = LayoutInflater.from(getContext()).inflate(R.layout.content, parent, false);
        }

        MovieData movie = getItem(position);
        if (movie != null) {
            ((TextView) convertView.findViewById(R.id.movie_text)).setText("🎬 " + movie.getTitle());
            ((TextView) convertView.findViewById(R.id.director_text)).setText("🎥 " + movie.getDirector());
            ((TextView) convertView.findViewById(R.id.genre_text)).setText("📚 " + movie.getGenre());
            ((TextView) convertView.findViewById(R.id.year_text)).setText("📅 " + movie.getYear());
            ((TextView) convertView.findViewById(R.id.watch_status)).setText(movie.isWatched() ? "✅ Watched" : "❌ Unwatched");
        }

        return convertView;
    }
}
