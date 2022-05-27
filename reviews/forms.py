from django import forms
from reviews.models import Review


class CreateReviewForm(forms.ModelForm):
    accuracy = forms.IntegerField(max_value=5, min_value=1)
    communication = forms.IntegerField(max_value=5, min_value=1)
    cleanliness = forms.IntegerField(max_value=5, min_value=1)
    location = forms.IntegerField(max_value=5, min_value=1)
    check_in = forms.IntegerField(max_value=5, min_value=1)
    value = forms.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = Review
        exclude = (
            "user",
            "room",
        )

    def save(self, room, user, commit=True):
        review = super().save(commit=False)
        review.room = room
        review.user = user
        if commit:
            review.save()
        return review
