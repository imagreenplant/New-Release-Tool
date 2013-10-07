from django import forms
from Tools import Tools
from newreleases.nrdb.models import Release, Batch, Idea

class BatchForm(forms.Form):
    batch_name = forms.CharField(max_length=40,label='Batch Name(optional):', required=False)
    release_id_string = forms.CharField(widget=forms.Textarea(attrs={'rows':'20'}),label='Release Ids (comma or line separated album ids):', required=True)
    error_ids = []
    created_batch_id = 0
    
    def testForValidIds(self):
        data = self.cleaned_data
        print "data is ", data
        Tool = Tools()
        self.release_ids = Tool.parseOutReleaseIds(data['release_id_string'])
        
        if self.release_ids:
            return True
        else:
            return False

    def save(self):
        #create new batch in database
        newbatch = Batch(name=self.cleaned_data['batch_name'])
        newbatch.save()
        
        self.created_batch_id = newbatch.id
        
        for r_id in self.release_ids:
            try:
                release = Release(release_id=r_id, description = 'none')
                release.save()
                release.batch.add(newbatch)
            except:
                self.error_ids.append(r_id)
        
        print "Error_ids", self.error_ids
            
class IdeaForm(forms.Form):
    idea_name = forms.CharField(widget=forms.Textarea(attrs={'rows':'20','cols':'20'}),label='Submit Idea here:', required=True)
    created_batch_id = 0

    def save(self):
        #create new idea in database
        data = self.cleaned_data
        newidea = Idea(name=self.cleaned_data['idea_name'])
        newidea.save()
