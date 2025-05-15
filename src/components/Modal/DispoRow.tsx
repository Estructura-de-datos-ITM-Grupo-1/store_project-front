import React, { ChangeEventHandler, useState } from 'react';
import { OrdersPallets } from '../../types/dispo';

type DispoRowProp = {
  index: number;
  initialValues: OrdersPallets;
  page: number;
  currentOrder: number;
  handleChangeDispo: (index: number, value: OrdersPallets) => void;
};

const DispoRow: React.FC<DispoRowProp> = ({
  index,
  initialValues,
  handleChangeDispo,
}) => {
  const [bigPallet, setBigPallet] = useState<number>(initialValues.bigPallets);
  const [littlePallets, setlittlePallets] = useState<number>(
    initialValues.littlePallets
  );

  const handleChangeBigPallet: ChangeEventHandler<HTMLInputElement> = (e) => {
    setBigPallet(Number(e.target.value));
    handleChangeDispo(index, {
      bigPallets: Number(e.target.value),
      littlePallets: littlePallets,
      dispoId: initialValues.dispoId,
    });
  };

  const handleChangeSmallPallet: ChangeEventHandler<HTMLInputElement> = (e) => {
    setlittlePallets(Number(e.target.value));
    handleChangeDispo(index, {
      bigPallets: bigPallet,
      littlePallets: Number(e.target.value),
      dispoId: initialValues.dispoId,
    });
  };

  return (
    <tr>
      <td>{initialValues.dispoId}</td>
      <td>
        <input
          type="text"
          placeholder="Pallets"
          value={bigPallet}
          className="bg-white border focus:border-red py-1 px-2 rounded-md text-center"
          onChange={handleChangeBigPallet}
        />
      </td>
      <td>
        <input
          type="text"
          placeholder="Pallets"
          value={littlePallets}
          onChange={handleChangeSmallPallet}
          className="bg-white border focus:border-red py-1 px-2 rounded-md text-center"
        />
      </td>
    </tr>
  );
};

export default DispoRow;
