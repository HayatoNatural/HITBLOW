import random
from typing import List,Tuple
import itertools
import argparse

class Numberguess:

    def __init__(self,max_count=100,ans=None) -> None:
        self.max_count = max_count
        self.digits = 5
        self.count = 0
        self.history = []
        self.list_where_num_is = []
        self.list_ans_num = []
        self.List_16 = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
        if ans is not None:
            self.ans = ans
        else:
            self.ans = self._define_answer()
        self.num = None
        self.hit = None
        self.blow = None

    def _define_answer(self) -> str:
        ans_list = random.sample(self.List_16, self.digits)
        ans = "".join(ans_list)
        return ans


    def _get_your_num(self) -> str :
        while True:
            num = input("16進数で5桁の重複しない数字を入力してください ==> ")
            judge = True
            for i in num:
                if i not in self.List_16:
                    judge = False
            if judge == True and len(num) == self.digits and len(set(num)) == self.digits:
                return num
            else:
                print("もう一度入力しなおしてください(16進数, 5桁, 重複なし)")

    def _show_hit_blow(self) -> None:
        self.hit = 0
        self.blow = 0
        for i in range(self.digits):
            if self.num[i] == self.ans[i]:
                self.hit += 1
            else:
                if self.num[i] in self.ans:
                    self.blow += 1


    def _play_game_manual(self) -> None:
        while self.count < self.max_count:
            print("残りの入力回数は{}回です".format(self.max_count-self.count))
            self.num = self._get_your_num()
            self.history.append(self.num)
            self.count += 1 
            self._show_hit_blow()
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.hit == 5:
                print("!! 正解です !!")
                break

    def _first_three_times(self):
        search_list = ["01234","56789","abcde"]
        for i in range(3):
            print("残りの入力回数は{}回です".format(self.max_count-self.count))
            self.num = search_list[i]
            self.history.append(self.num)
            self.count += 1
            self._show_hit_blow()
            self.list_where_num_is.append(self.hit + self.blow)
            print("-----",self.num)
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.hit == 5:
                print("!! 正解です !!")
                break

    def _search_5_combination(self):
        for i in itertools.combinations("01234", self.list_where_num_is[0]):
            for j in itertools.combinations("56789", self.list_where_num_is[1]):
                for k in itertools.combinations("abcde", self.list_where_num_is[2]):
                    for l in itertools.combinations("f", self.digits-sum(self.list_where_num_is)):                
                        print("残りの入力回数は{}回です".format(self.max_count-self.count))
                        self.num = "".join(i+j+k+l)
                        self.history.append(self.num)
                        self.count += 1
                        self._show_hit_blow()
                        print("-----",self.num)
                        print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
                        if self.hit == 5:
                            print("!! 正解です !!")
                            break
                        elif self.hit + self.blow == 5:
                            self.list_ans_num = [i for i in self.num]
                            break
                    if self.hit + self.blow == 5:
                        break
                if self.hit + self.blow == 5:
                    break
            if self.hit + self.blow == 5:
                break

    # def _sum_hitblow_4(self):
    #     for i in self.num:
    #         for j in list(set(self.List_16) ^ set(list(self.num))):
    #             new_num = 


    def _determine_permutation(self):
        for i in itertools.permutations(self.list_ans_num, self.digits):
            print("残りの入力回数は{}回です".format(self.max_count-self.count))
            self.num = "".join(i)
            self.history.append(self.num)
            self.count += 1
            self._show_hit_blow()
            print("-----",self.num)
            print("!!  {} Hit, {} Blow  !!".format(self.hit,self.blow))
            if self.hit == 5:
                print("!! 正解です !!")
                break

    
    def _play_game_auto(self):
        self._first_three_times()
        self._search_5_combination()
        self._determine_permutation()


    def run(self, mode="auto") -> Tuple[int,List[int]]:
        """ 数当てゲーム実行ランナー
        : param str mode : ゲームの実行モード("manual","linear","binary")
        : rtype : None
        : return : なし
        """

        if mode == "auto":
            self._play_game_auto()
        else:
            self._play_game_manual()
        self._show_result()


    def _show_result(self) -> None:
        print("------------------------")
        print("show history")
        for k,v in enumerate(self.history):
            print("{}回目 : {} ".format(k+1,v))

        print("------------------------")
        if self.history[-1] == self.ans:
            print("正解は{}です. おめでとうございます！ {}回で正解しました.".format(self.ans,self.count))
        else:
            print("正解は{}でした".format(self.ans))

        print("------------------------")

def get_parser() -> argparse.Namespace:
    """コマンドライン引数を解析したものを持つ

    """
    parser = argparse.ArgumentParser(description="Hit&Blow, 数当てゲーム")
    parser.add_argument("--max_count",default=700)
    parser.add_argument("--ans")
    parser.add_argument("--mode",default="auto")
    args = parser.parse_args()
    return args

def main():
    """数当てゲームのメイン
    """
    args = get_parser()
    mode = args.mode
    max_count = int(args.max_count)
    ans= args.ans
    if args.ans is not None:
        runner = Numberguess(max_count=max_count,ans=ans)
    else:
        runner = Numberguess(max_count=max_count)

    runner.run(mode=mode)
    # print(runner.list_ans_num)

if __name__ == "__main__":
    main()
