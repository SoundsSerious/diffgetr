import deepdiff
import sys
import json
import io
import re
import argparse
from pprint import pprint

class diff_get:
    
    def __init__(self,s0,s1,loc=None,path=None,deep_diff_kw=None,ignore_added=True):
        self.s0 = s0
        self.s1 = s1
        self.ignore_added = ignore_added
        if deep_diff_kw is None:
            self.deep_diff_kw = dict(ignore_numeric_type_changes=True,significant_digits =3)
        else:
            self.deep_diff_kw = deep_diff_kw

        if loc is None:
            self.loc = []
        else:
            self.loc = loc
        if path is not None:
            self.loc.append(path)
        else:
            self.loc=['root']
        
    def __getitem__(self,key):
        if key in self.s0 and key in self.s1:
            return diff_get(self.s0[key],self.s1[key],path=key,loc=self.loc.copy(),ignore_added=self.ignore_added,deep_diff_key=self.deep_diff_kw)
        else:
            #self.diff_data(sys.stdout,bytes=False)
            self.diff_summary()
            raise KeyError(f'{self.location} | key missing: {key}')
            
    @property
    def location(self):
        return '.'.join(self.loc)
    
    def __repr__(self):
        return f'diff[{self.location}]'

    def __str__(self):
        fil = io.BytesIO()
        out = self.diff_summary(fil,top=10)
        fil.seek(0)
        buff = fil.getvalue().decode('utf-8')
        return buff

    @property
    def diff_obj(self) -> deepdiff.DeepDiff:
        df = deepdiff.DeepDiff(self.s0,self.s1, **self.deep_diff_kw)
        if self.ignore_added:
            for k in list(df):
                if 'added' in k:
                    df.pop(k)
        return df


    def diff_all(self,indent=2):
        df = self.diff_obj
        pprint(df,indent=indent)

    def diff_summary(self,file=None,top=50,bytes=None):

        if file is None:
            file = sys.stdout
            bytes = False
        elif bytes is None:
            if hasattr(file, 'mode'):
                bytes = 'b' in file.mode
            else:
                # Fallback: check if file expects bytes by writing a test string
                try:
                    file.write(b'')  # Try writing empty bytes
                    bytes = True
                except TypeError:
                    bytes = False


        df = self.diff_obj

        title = f'{self.location} diffing data\n\n'
        file.write(title.encode('utf-8') if bytes else title)
        uuid_word = re.compile(
            "[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"
        )
        comp = "[0-9\.]*(,[0-9\.]+)+"
        csv_word = re.compile(comp)
        key_counts = {}
        all_sys_keys = set()
        sys_keys = {}
        for gk,cats in df.items():
            if isinstance(cats,dict):
                cats = list(cats.keys())
            sys_kf = [re.sub(csv_word,"<CSV>",re.sub(uuid_word, "<UUID>", v)) for v in cats]
            sys_refs = [tuple(c.replace("']","").replace('root.','').split("['")) for c in sys_kf]
            kc = key_counts.get(gk,{})
            for grps in sys_refs:
                L = len(grps)
                for i in range(L-1):
                    wrds = tuple(grps[:L+1-i])
                    all_sys_keys.add(wrds)
                    seg_key = '.'.join(wrds)
                    kc[seg_key] = kc.get(seg_key,0) + 1
        
            key_counts[gk] = kc
        
        for k,v in key_counts.items():
            v = sorted(v.items(),key=lambda kv: kv[-1])
            tc = sum([vi[-1] for vi in v])
            t = f'{k.upper():<100}|{tc}\n'
            file.write(t.encode('utf-8') if bytes else t)
            for key,num in v[-top:]:
                f = f'{key:<100}|{num}\n'
                file.write(f.encode('utf-8') if bytes else f)
            file.write(('\n'*2).encode('utf-8') if bytes else '\n'*2)


def main():
    parser = argparse.ArgumentParser(description="Diff two JSON files and navigate to a specific path.")
    parser.add_argument("file1", help="First JSON file")
    parser.add_argument("file2", help="Second JSON file")
    parser.add_argument("path", help="Dot-separated path to navigate in the JSON structure")

    args = parser.parse_args()

    with open(args.file1, 'r', encoding='utf-8') as f:
        s0 = json.load(f)
    with open(args.file2, 'r', encoding='utf-8') as f:
        s1 = json.load(f)

    DIFF = diff_get(s0, s1)
    keys = args.path.split('.')
    try:
        for key in keys:
            if key.endswith(']') and '[' in key:
                base, idx = key.rsplit('[', 1)
                idx = int(idx[:-1])
                DIFF = DIFF[base]
                loc = DIFF.loc.copy()
                loc.append(f'[{idx}]')
                DIFF = diff_get(DIFF.s0[idx],DIFF.s1[idx],loc=loc)
                continue
            else:
                DIFF = DIFF[key]

        print(DIFF)
        
    except KeyError:
        # diff_data already prints to stdout in __getitem__ on KeyError
        pass

    if __name__ == "__main__":
        main()