from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm, PostCreateForm
from django.utils.text import slugify


# Create your views here.


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        #posts = Post.objects.order_by('-created')
        #order_by mesl all amal mikone va hamaro miyare vali mitonim behesh shart bedim
        #chera - ? ax mikone natije ro
        #posts = Post.objects.order_by('?')
        #entekhab random --> sorat barname ro miyare payin
        # vali baraye inke in tartib hameja emal beshe mizarimesh to model ha ye class meta barash tarif mikonim
        return render(request, 'home/index.html', {'posts': posts})


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        #aslesh bayad in bashe vali mikham befahme age on post vojod nadasht bere safe error 404
        #post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'home/detail.html', {'post': post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        #post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'post deleted', 'success')
        else:
            messages.error(request, 'you can delete this post', 'danger')
        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostUpdateForm

    # setup ro minevisam ke kolan ye bar vasl sham b database na 100 bar
    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        #self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    # hamishe setup ro aval benevis
    # dispatch ro minevisam ke kod tekrari nadashte basham

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, 'you cant update this post', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # chera parametr bala ro post_id ersal nakardim o *args gozashtim?
        # chon ke momkene koli moteghayer dashte bashim ke bekhaym pas bedim behtare az in ravesh estefade konim
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            # yani sabr kon save nakon
            # chera in karo mikonim? chon ke bayad slug besazim az body va onam update she
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.save()
            messages.success(request, 'you update this post', 'success')
            return redirect('home:post_detail', post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            # yani sabr kon save nakon
            # chera in karo mikonim? chon ke bayad slug besazim az body va onam update she
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'you create new post', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)
