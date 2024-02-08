import { atom, selector } from "recoil";
import { recoilPersist } from "recoil-persist";
import { WalletType } from "../types/wallet";

const { persistAtom } = recoilPersist();

export const walletState = atom<WalletType | null>({
  key: "WalletState",
  default: null,
  effects_UNSTABLE: [persistAtom],
});
