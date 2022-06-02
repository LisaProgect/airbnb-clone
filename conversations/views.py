from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import View
from django.db.models import Q
from django.urls import reverse
from users.models import User
from conversations.models import Conversation, Message


def go_conversation(request, host_pk, guest_pk):
    host = User.objects.get_or_none(pk=host_pk)
    guest = User.objects.get_or_none(pk=guest_pk)
    if host is not None and guest is not None:
        conversation = Conversation.objects.filter(
            Q(participants=host) & Q(participants=guest)
        )
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(host, guest)
        return redirect(reverse("conversations:detail", kwargs={"pk": conversation.pk}))


class ConversationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        return render(
            self.request,
            "conversations/conversation_detail.html",
            {"conversation": conversation},
        )

    def post(self, *args, **kwargs):
        message = self.request.POST.get("message", None)
        pk = kwargs.get("pk")
        conversation = Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()
        if message is not None:
            Message.objects.create(
                message=message, user=self.request.user, conversation=conversation
            )
        return redirect(reverse("conversations:detail", kwargs={"pk": pk}))
